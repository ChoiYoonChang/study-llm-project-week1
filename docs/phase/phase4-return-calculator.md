# Phase 4: 암호화폐 수익률 계산기 구현 (도전 과제)

## 📋 진행 체크리스트

### 1. 과거 데이터 조회 시스템 구현
- [ ] 업비트 일봉 API 연동 함수 (`get_historical_data_api`)
- [ ] 날짜 계산 및 데이터 필터링 로직
- [ ] API 응답 데이터 파싱 및 검증

### 2. 투자 시점 가격 추출 로직
- [ ] 지정한 일수 전 가격 추출
- [ ] 날짜 매칭 및 유효성 검증
- [ ] 주말/공휴일 처리 로직

### 3. 현재가 조회 및 비교 시스템
- [ ] 단일 암호화폐 현재가 조회 재활용
- [ ] 투자 시점 가격과 현재가 비교
- [ ] 데이터 일관성 검증

### 4. 수익률 계산 엔진 구현
- [ ] 구매 수량 계산 (투자금액 ÷ 투자시점가격)
- [ ] 현재 가치 계산 (구매수량 × 현재가)
- [ ] 손익 및 수익률 계산
- [ ] 복리 수익률 계산 (추가 기능)

### 5. 결과 출력 및 분석 기능
- [ ] 투자 결과 상세 정보 출력
- [ ] 수익률 시각적 표시
- [ ] 투자 성과 평가 메시지

### 6. 사용자 인터페이스 구현
- [ ] 투자 조건 입력 시스템
- [ ] 프리셋 투자 시나리오 제공
- [ ] 다중 시나리오 비교 기능

### 7. 테스트 및 검증
- [ ] 다양한 기간별 수익률 계산 테스트
- [ ] 손실 시나리오 테스트
- [ ] 경계값 및 예외 상황 테스트

---

## 📁 생성할 파일

### 1. src/return_calculator.py (메인 구현 파일)
### 2. tests/test_return_calculator.py (테스트 파일)

---

## 📝 상세 구현 계획

### 1. src/return_calculator.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/src/return_calculator.py`

**파일 내용**:
```python
"""
암호화폐 수익률 계산기
과거 특정 시점에 투자했다면 현재 수익률이 얼마인지 계산
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple
from utils.api_client import get_historical_data, get_single_price
from utils.date_utils import get_date_days_ago, format_date, parse_upbit_datetime
from utils.format_utils import (
    format_currency,
    format_percentage,
    format_crypto_amount,
    create_table_header,
    create_table_row
)
from config.settings import DEFAULT_CRYPTOS


def get_historical_data_api(market: str, days_count: int) -> Optional[List[Dict]]:
    """
    업비트 API를 통해 과거 일봉 데이터를 조회

    Args:
        market (str): 마켓 코드 (예: 'KRW-BTC')
        days_count (int): 조회할 일수

    Returns:
        List[Dict]: 일봉 데이터 리스트 (최신순)
        None: 조회 실패시
    """
    print(f"📡 {market}의 최근 {days_count}일 데이터 조회 중...")

    try:
        historical_data = get_historical_data(market, days_count)

        if not historical_data:
            print(f"❌ {market}의 과거 데이터 조회에 실패했습니다.")
            return None

        print(f"✅ {len(historical_data)}일분 데이터 조회 완료")
        return historical_data

    except Exception as e:
        print(f"❌ 과거 데이터 조회 중 오류 발생: {e}")
        return None


def get_single_price_api(market: str) -> Optional[float]:
    """
    단일 암호화폐의 현재가를 조회 (재사용)

    Args:
        market (str): 마켓 코드

    Returns:
        float: 현재가
        None: 조회 실패시
    """
    try:
        current_price = get_single_price(market)
        return current_price
    except Exception as e:
        print(f"❌ 현재가 조회 오류 ({market}): {e}")
        return None


def find_investment_date_price(historical_data: List[Dict], days_ago: int) -> Optional[Tuple[float, str]]:
    """
    지정한 일수 전의 가격을 찾아 반환

    Args:
        historical_data (List[Dict]): 일봉 데이터
        days_ago (int): 며칠 전

    Returns:
        Tuple[float, str]: (가격, 날짜) 또는 None
    """
    if not historical_data or days_ago < 1:
        return None

    # 데이터 길이 확인
    if len(historical_data) < days_ago:
        print(f"⚠️  요청한 기간({days_ago}일)의 데이터가 부족합니다. 사용 가능: {len(historical_data)}일")
        return None

    try:
        # 업비트 API는 최신순으로 데이터를 반환하므로 인덱스 days_ago-1 사용
        target_data = historical_data[days_ago - 1]

        # 필요한 데이터 추출
        candle_date = target_data.get('candle_date_time_kst', '')
        trade_price = target_data.get('trade_price', 0)

        if not trade_price:
            print(f"❌ {days_ago}일 전 가격 데이터가 유효하지 않습니다.")
            return None

        # 날짜 형식 변환
        formatted_date = candle_date.split('T')[0] if 'T' in candle_date else candle_date

        return float(trade_price), formatted_date

    except (IndexError, KeyError, ValueError) as e:
        print(f"❌ 투자 시점 가격 추출 오류: {e}")
        return None


def calculate_investment_return(market: str, days_ago: int, investment_amount: float) -> Dict[str, Any]:
    """
    투자 수익률을 계산하는 메인 함수

    Args:
        market (str): 마켓 코드
        days_ago (int): 투자 시점 (며칠 전)
        investment_amount (float): 투자 금액

    Returns:
        Dict[str, Any]: 계산 결과
    """
    print(f"\n🔍 {market} {days_ago}일 전 투자 시나리오 분석 시작...")

    # 1. 입력 데이터 검증
    if days_ago < 1:
        return {
            'success': False,
            'error_message': '투자 시점은 1일 이상이어야 합니다.',
            'market': market
        }

    if investment_amount <= 0:
        return {
            'success': False,
            'error_message': '투자 금액은 0보다 커야 합니다.',
            'market': market
        }

    # 2. 과거 데이터 조회
    historical_data = get_historical_data_api(market, days_ago + 5)  # 여유분 포함
    if not historical_data:
        return {
            'success': False,
            'error_message': '과거 데이터 조회에 실패했습니다.',
            'market': market
        }

    # 3. 투자 시점 가격 추출
    investment_data = find_investment_date_price(historical_data, days_ago)
    if not investment_data:
        return {
            'success': False,
            'error_message': f'{days_ago}일 전 가격 데이터를 찾을 수 없습니다.',
            'market': market
        }

    investment_price, investment_date = investment_data

    # 4. 현재가 조회
    current_price = get_single_price_api(market)
    if current_price is None:
        return {
            'success': False,
            'error_message': '현재가 조회에 실패했습니다.',
            'market': market
        }

    # 5. 수익률 계산
    try:
        # 구매 수량 = 투자 금액 ÷ 투자 시점 가격
        purchase_quantity = investment_amount / investment_price

        # 현재 가치 = 구매 수량 × 현재가
        current_value = purchase_quantity * current_price

        # 손익 = 현재 가치 - 투자 금액
        profit_loss = current_value - investment_amount

        # 수익률 = (손익 ÷ 투자 금액) × 100
        return_rate = (profit_loss / investment_amount) * 100

        # 연간 수익률 (복리) 계산
        annual_return_rate = calculate_annual_return_rate(return_rate, days_ago)

        coin_name = market.split('-')[1]

        return {
            'success': True,
            'error_message': '',
            'market': market,
            'coin_name': coin_name,
            'investment_date': investment_date,
            'investment_amount': investment_amount,
            'investment_price': investment_price,
            'purchase_quantity': purchase_quantity,
            'current_price': current_price,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'return_rate': return_rate,
            'annual_return_rate': annual_return_rate,
            'days_ago': days_ago,
            'is_profit': profit_loss > 0
        }

    except ZeroDivisionError:
        return {
            'success': False,
            'error_message': '투자 시점 가격이 0입니다.',
            'market': market
        }
    except Exception as e:
        return {
            'success': False,
            'error_message': f'계산 중 오류 발생: {e}',
            'market': market
        }


def calculate_annual_return_rate(return_rate: float, days: int) -> float:
    """
    연간 수익률(복리)을 계산

    Args:
        return_rate (float): 기간 수익률 (%)
        days (int): 투자 기간 (일)

    Returns:
        float: 연간 수익률 (%)
    """
    try:
        if days <= 0:
            return 0

        # 일일 수익률 계산
        daily_return = return_rate / 100 / days

        # 연간 수익률 (복리) = (1 + 일일수익률)^365 - 1
        annual_return = (1 + daily_return) ** 365 - 1

        return annual_return * 100

    except Exception:
        return 0


def print_investment_result(result: Dict[str, Any]) -> None:
    """
    투자 수익률 계산 결과를 출력

    Args:
        result (Dict): calculate_investment_return의 결과
    """
    if not result['success']:
        print(f"\n❌ 계산 실패: {result['error_message']}")
        return

    # 수익/손실에 따른 이모지 및 색상 표시
    profit_emoji = "📈" if result['is_profit'] else "📉"
    status_text = "수익" if result['is_profit'] else "손실"

    print(f"\n" + "="*70)
    print(f"{profit_emoji} {result['coin_name']} 투자 수익률 분석 결과")
    print(f"="*70)

    # 기본 정보
    print(f"🪙 암호화폐: {result['coin_name']} ({result['market']})")
    print(f"📅 투자 일자: {result['investment_date']} ({result['days_ago']}일 전)")
    print(f"💰 투자 금액: {format_currency(result['investment_amount'])}")

    print(f"\n📊 가격 정보:")
    print(f"   투자시점 가격: {format_currency(result['investment_price'])}")
    print(f"   현재 가격: {format_currency(result['current_price'])}")

    # 가격 변화율
    price_change_rate = ((result['current_price'] - result['investment_price']) / result['investment_price']) * 100
    price_change_emoji = "⬆️" if price_change_rate > 0 else "⬇️" if price_change_rate < 0 else "➡️"
    print(f"   가격 변화: {price_change_emoji} {format_percentage(abs(price_change_rate))}")

    print(f"\n🔢 투자 분석:")
    print(f"   구매 수량: {format_crypto_amount(result['purchase_quantity'])}")
    print(f"   현재 가치: {format_currency(result['current_value'])}")

    # 손익 및 수익률
    profit_sign = "+" if result['is_profit'] else ""
    print(f"\n💵 손익 분석:")
    print(f"   손익 금액: {profit_sign}{format_currency(result['profit_loss'])}")
    print(f"   수익률: {profit_sign}{format_percentage(result['return_rate'])}")
    print(f"   연간 수익률: {profit_sign}{format_percentage(result['annual_return_rate'])} (복리 기준)")

    # 투자 성과 평가
    print(f"\n📝 투자 성과 평가:")
    if result['return_rate'] > 20:
        print(f"   🎉 대박! 매우 높은 수익률을 기록했습니다!")
    elif result['return_rate'] > 10:
        print(f"   🎊 훌륭한 수익률입니다!")
    elif result['return_rate'] > 0:
        print(f"   😊 수익을 실현했습니다.")
    elif result['return_rate'] > -10:
        print(f"   😐 소폭 손실이 발생했습니다.")
    elif result['return_rate'] > -20:
        print(f"   😰 상당한 손실이 발생했습니다.")
    else:
        print(f"   😱 큰 손실이 발생했습니다.")

    print(f"="*70)


def get_user_investment_settings() -> Optional[Dict[str, Any]]:
    """
    사용자로부터 투자 조건을 입력받는 함수

    Returns:
        Dict[str, Any]: 투자 설정 정보
        None: 입력 실패시
    """
    print(f"\n📝 투자 수익률 계산 설정을 입력해주세요")
    print(f"-" * 50)

    try:
        # 암호화폐 선택
        print(f"📈 추천 암호화폐:")
        for i, crypto in enumerate(DEFAULT_CRYPTOS[:5], 1):
            coin_name = crypto.split('-')[1]
            print(f"   {i}. {coin_name} ({crypto})")

        market_input = input(f"\n마켓 코드 입력 (예: KRW-BTC): ").strip().upper()

        if not market_input.startswith('KRW-'):
            print("❌ KRW 마켓만 지원합니다.")
            return None

        # 투자 시점 입력
        while True:
            try:
                days_ago = int(input(f"투자 시점 입력 (며칠 전, 1-365): "))
                if not 1 <= days_ago <= 365:
                    print("❌ 1일에서 365일 사이로 입력해주세요.")
                    continue
                break
            except ValueError:
                print("❌ 숫자를 입력해주세요.")

        # 투자 금액 입력
        while True:
            try:
                investment_amount = float(input(f"투자 금액 입력 (원): "))
                if investment_amount <= 0:
                    print("❌ 투자 금액은 0보다 커야 합니다.")
                    continue
                break
            except ValueError:
                print("❌ 숫자를 입력해주세요.")

        return {
            'market': market_input,
            'days_ago': days_ago,
            'investment_amount': investment_amount
        }

    except KeyboardInterrupt:
        print("\n❌ 설정이 취소되었습니다.")
        return None


def get_preset_investment_scenarios() -> List[Dict[str, Any]]:
    """
    미리 설정된 투자 시나리오들을 반환

    Returns:
        List[Dict]: 프리셋 시나리오 리스트
    """
    return [
        {
            'name': '1주일 전 비트코인 100만원',
            'market': 'KRW-BTC',
            'days_ago': 7,
            'investment_amount': 1000000
        },
        {
            'name': '1개월 전 이더리움 500만원',
            'market': 'KRW-ETH',
            'days_ago': 30,
            'investment_amount': 5000000
        },
        {
            'name': '3개월 전 리플 200만원',
            'market': 'KRW-XRP',
            'days_ago': 90,
            'investment_amount': 2000000
        },
        {
            'name': '6개월 전 에이다 300만원',
            'market': 'KRW-ADA',
            'days_ago': 180,
            'investment_amount': 3000000
        }
    ]


def compare_multiple_scenarios(scenarios: List[Dict[str, Any]]) -> None:
    """
    여러 투자 시나리오를 비교 분석

    Args:
        scenarios (List[Dict]): 시나리오 리스트
    """
    print(f"\n🔍 다중 시나리오 비교 분석")
    print(f"=" * 80)

    results = []

    for scenario in scenarios:
        print(f"\n📊 {scenario['name']} 분석 중...")
        result = calculate_investment_return(
            market=scenario['market'],
            days_ago=scenario['days_ago'],
            investment_amount=scenario['investment_amount']
        )

        if result['success']:
            results.append(result)
        else:
            print(f"❌ {scenario['name']} 분석 실패: {result['error_message']}")

    if not results:
        print("❌ 비교할 수 있는 결과가 없습니다.")
        return

    # 결과 테이블 출력
    print(f"\n📋 시나리오 비교 결과")
    print(f"-" * 80)

    # 테이블 헤더
    columns = ['암호화폐', '투자기간', '투자금액', '현재가치', '손익', '수익률']
    widths = [10, 12, 12, 12, 12, 10]
    alignments = ['center', 'center', 'right', 'right', 'right', 'center']

    print(create_table_header(columns, widths))

    # 수익률 순으로 정렬
    sorted_results = sorted(results, key=lambda x: x['return_rate'], reverse=True)

    for result in sorted_results:
        profit_sign = "+" if result['is_profit'] else ""
        values = [
            result['coin_name'],
            f"{result['days_ago']}일전",
            format_currency(result['investment_amount']),
            format_currency(result['current_value']),
            f"{profit_sign}{format_currency(result['profit_loss'])}",
            f"{profit_sign}{format_percentage(result['return_rate'])}"
        ]
        print(create_table_row(values, widths, alignments))

    # 통계 요약
    total_investment = sum(r['investment_amount'] for r in results)
    total_current_value = sum(r['current_value'] for r in results)
    total_profit_loss = total_current_value - total_investment
    total_return_rate = (total_profit_loss / total_investment) * 100

    print("|" + "-" * 78 + "|")
    total_row = [
        "전체 합계",
        f"{len(results)}건",
        format_currency(total_investment),
        format_currency(total_current_value),
        f"{'+' if total_profit_loss > 0 else ''}{format_currency(total_profit_loss)}",
        f"{'+' if total_return_rate > 0 else ''}{format_percentage(total_return_rate)}"
    ]
    print(create_table_row(total_row, widths, alignments))

    # 최고/최저 수익률
    best_result = max(results, key=lambda x: x['return_rate'])
    worst_result = min(results, key=lambda x: x['return_rate'])

    print(f"\n🏆 최고 수익률: {best_result['coin_name']} {format_percentage(best_result['return_rate'])}")
    print(f"📉 최저 수익률: {worst_result['coin_name']} {format_percentage(worst_result['return_rate'])}")


def run_return_calculator():
    """
    수익률 계산기 메인 실행 함수
    """
    print(f"\n" + "="*70)
    print(f"📈 암호화폐 수익률 계산기")
    print(f"="*70)
    print(f"과거 특정 시점에 투자했다면 현재 수익률이 얼마인지 계산합니다.")

    # 실행 모드 선택
    print(f"\n실행 모드를 선택하세요:")
    print(f"1. 단일 시나리오 계산 (직접 입력)")
    print(f"2. 프리셋 시나리오 비교")
    print(f"3. 커스텀 다중 시나리오")

    try:
        choice = input("선택 (1-3): ").strip()

        if choice == '1':
            # 단일 시나리오
            settings = get_user_investment_settings()
            if settings is None:
                print("❌ 설정을 완료하지 못했습니다.")
                return

            result = calculate_investment_return(
                market=settings['market'],
                days_ago=settings['days_ago'],
                investment_amount=settings['investment_amount']
            )

            print_investment_result(result)

        elif choice == '2':
            # 프리셋 시나리오 비교
            scenarios = get_preset_investment_scenarios()
            print(f"\n📊 프리셋 시나리오들을 분석합니다:")
            for scenario in scenarios:
                print(f"   - {scenario['name']}")

            compare_multiple_scenarios(scenarios)

        elif choice == '3':
            # 커스텀 다중 시나리오
            print(f"\n📝 여러 시나리오를 입력해주세요 (최대 5개)")
            scenarios = []

            for i in range(5):
                print(f"\n--- 시나리오 {i+1} ---")
                print(f"(입력하지 않으면 종료)")

                settings = get_user_investment_settings()
                if settings is None:
                    break

                scenarios.append({
                    'name': f"시나리오{i+1}: {settings['market']} {settings['days_ago']}일전",
                    **settings
                })

                if i < 4:
                    continue_input = input("\n다음 시나리오를 입력하시겠습니까? (y/n): ").strip().lower()
                    if continue_input != 'y':
                        break

            if scenarios:
                compare_multiple_scenarios(scenarios)
            else:
                print("❌ 입력된 시나리오가 없습니다.")

        else:
            print("❌ 잘못된 선택입니다.")

    except KeyboardInterrupt:
        print("\n❌ 프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    # 직접 실행시 테스트
    run_return_calculator()
```

**작성 이유**:
- **포괄적 기능**: 단일/다중 시나리오 분석으로 다양한 사용자 요구 충족
- **정확한 계산**: 복리 연간 수익률 등 전문적인 투자 지표 제공
- **데이터 검증**: 과거 데이터의 유효성과 일관성을 철저히 검증
- **사용자 친화적**: 프리셋 시나리오와 직접 입력 모드로 편의성 제공
- **비교 분석**: 여러 투자 시나리오를 동시에 비교하여 통찰 제공
- **투자 평가**: 수익률에 따른 정성적 평가 메시지로 결과 해석 도움

### 2. tests/test_return_calculator.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/tests/test_return_calculator.py`

**파일 내용**:
```python
"""
수익률 계산기 테스트 파일
다양한 투자 시나리오와 계산 로직을 테스트
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.return_calculator import (
    calculate_investment_return,
    calculate_annual_return_rate,
    find_investment_date_price,
    get_historical_data_api,
    get_single_price_api
)


def test_annual_return_calculation():
    """연간 수익률 계산 함수 테스트"""
    print("\n🧪 연간 수익률 계산 테스트")
    print("-" * 40)

    test_cases = [
        (10, 30, "1개월 10% 수익"),    # 30일에 10% 수익
        (20, 90, "3개월 20% 수익"),    # 90일에 20% 수익
        (-10, 30, "1개월 10% 손실"),   # 30일에 10% 손실
        (50, 365, "1년 50% 수익"),     # 365일에 50% 수익
        (5, 7, "1주일 5% 수익")        # 7일에 5% 수익
    ]

    for return_rate, days, description in test_cases:
        annual_rate = calculate_annual_return_rate(return_rate, days)
        print(f"📊 {description}")
        print(f"   기간 수익률: {return_rate}% ({days}일)")
        print(f"   연간 수익률: {annual_rate:.2f}%")
        print()


def test_api_connections():
    """API 연결 테스트"""
    print("\n🌐 API 연결 테스트")
    print("-" * 40)

    # 현재가 조회 테스트
    test_market = "KRW-BTC"
    current_price = get_single_price_api(test_market)

    if current_price:
        print(f"✅ 현재가 조회 성공: {test_market} = {current_price:,}원")
    else:
        print(f"❌ 현재가 조회 실패: {test_market}")

    # 과거 데이터 조회 테스트
    historical_data = get_historical_data_api(test_market, 10)

    if historical_data:
        print(f"✅ 과거 데이터 조회 성공: {len(historical_data)}일분 데이터")

        # 첫 번째와 마지막 데이터 확인
        if len(historical_data) > 0:
            latest = historical_data[0]
            oldest = historical_data[-1]
            print(f"   최신: {latest.get('candle_date_time_kst', '')[:10]} - {latest.get('trade_price', 0):,}원")
            print(f"   가장 오래된: {oldest.get('candle_date_time_kst', '')[:10]} - {oldest.get('trade_price', 0):,}원")
    else:
        print(f"❌ 과거 데이터 조회 실패: {test_market}")


def test_investment_date_price_extraction():
    """투자 시점 가격 추출 테스트"""
    print("\n📅 투자 시점 가격 추출 테스트")
    print("-" * 40)

    # 실제 데이터로 테스트
    market = "KRW-BTC"
    historical_data = get_historical_data_api(market, 10)

    if not historical_data:
        print("❌ 과거 데이터를 가져올 수 없어 테스트를 건너뜁니다.")
        return

    # 다양한 일수로 테스트
    test_days = [1, 3, 7, 10]

    for days_ago in test_days:
        result = find_investment_date_price(historical_data, days_ago)

        if result:
            price, date = result
            print(f"✅ {days_ago}일 전: {date} - {price:,}원")
        else:
            print(f"❌ {days_ago}일 전: 데이터 없음")


def test_investment_calculation():
    """투자 수익률 계산 테스트"""
    print("\n💰 투자 수익률 계산 테스트")
    print("-" * 40)

    # 실제 시나리오로 테스트
    test_scenarios = [
        ("KRW-BTC", 7, 1000000, "1주일 전 비트코인 100만원"),
        ("KRW-ETH", 30, 2000000, "1개월 전 이더리움 200만원")
    ]

    for market, days_ago, amount, description in test_scenarios:
        print(f"🔍 {description} 테스트:")

        result = calculate_investment_return(market, days_ago, amount)

        if result['success']:
            print(f"✅ 계산 성공")
            print(f"   투자 시점: {result['investment_date']}")
            print(f"   투자 가격: {result['investment_price']:,}원")
            print(f"   현재 가격: {result['current_price']:,}원")
            print(f"   구매 수량: {result['purchase_quantity']:.8f}")
            print(f"   현재 가치: {result['current_value']:,}원")
            print(f"   손익: {result['profit_loss']:,}원")
            print(f"   수익률: {result['return_rate']:.2f}%")
            print(f"   연간 수익률: {result['annual_return_rate']:.2f}%")
        else:
            print(f"❌ 계산 실패: {result['error_message']}")

        print()


def test_edge_cases():
    """경계값 및 특수 케이스 테스트"""
    print("\n🔍 경계값 테스트")
    print("-" * 40)

    # 매우 작은 투자 금액
    print("💰 매우 작은 투자 금액 테스트 (1원):")
    result = calculate_investment_return("KRW-BTC", 7, 1)
    success_status = "성공" if result['success'] else "실패"
    print(f"   결과: {success_status}")
    if result['success']:
        print(f"   구매 수량: {result['purchase_quantity']:.10f}")

    # 매우 큰 투자 금액
    print("\n💰 매우 큰 투자 금액 테스트 (100억원):")
    result = calculate_investment_return("KRW-BTC", 7, 10000000000)
    success_status = "성공" if result['success'] else "실패"
    print(f"   결과: {success_status}")
    if result['success']:
        print(f"   현재 가치: {result['current_value']:,.0f}원")

    # 매우 먼 과거 (1년 전)
    print("\n📅 1년 전 투자 테스트:")
    result = calculate_investment_return("KRW-BTC", 365, 1000000)
    success_status = "성공" if result['success'] else "실패"
    print(f"   결과: {success_status}")
    if not result['success']:
        print(f"   오류: {result['error_message']}")

    # 잘못된 입력값들
    print("\n❌ 잘못된 입력값 테스트:")

    # 음수 일수
    result = calculate_investment_return("KRW-BTC", -1, 1000000)
    print(f"   음수 일수: {'올바르게 거부됨' if not result['success'] else '예상과 다름'}")

    # 0 투자 금액
    result = calculate_investment_return("KRW-BTC", 7, 0)
    print(f"   0 투자금액: {'올바르게 거부됨' if not result['success'] else '예상과 다름'}")

    # 존재하지 않는 마켓
    result = calculate_investment_return("KRW-FAKE", 7, 1000000)
    print(f"   가짜 마켓: {'올바르게 거부됨' if not result['success'] else '예상과 다름'}")


def test_calculation_accuracy():
    """계산 정확성 테스트"""
    print("\n🔢 계산 정확성 테스트")
    print("-" * 40)

    # 알려진 값으로 수동 계산 검증
    print("📊 수동 계산 검증:")

    # 가상의 정확한 값들로 테스트
    investment_amount = 1000000  # 100만원
    investment_price = 50000000  # 5천만원
    current_price = 55000000     # 5천5백만원

    # 예상 계산 결과
    expected_quantity = investment_amount / investment_price  # 0.02
    expected_current_value = expected_quantity * current_price  # 1,100,000
    expected_profit = expected_current_value - investment_amount  # 100,000
    expected_return_rate = (expected_profit / investment_amount) * 100  # 10%

    print(f"   투자금액: {investment_amount:,}원")
    print(f"   투자가격: {investment_price:,}원")
    print(f"   현재가격: {current_price:,}원")
    print(f"   예상 수량: {expected_quantity:.8f}")
    print(f"   예상 현재가치: {expected_current_value:,}원")
    print(f"   예상 수익률: {expected_return_rate}%")

    # 연간 수익률 계산 정확성 테스트 (30일 기준)
    annual_rate = calculate_annual_return_rate(10, 30)  # 30일에 10%
    print(f"   30일 10% → 연간: {annual_rate:.2f}%")


def test_data_consistency():
    """데이터 일관성 테스트"""
    print("\n🔄 데이터 일관성 테스트")
    print("-" * 40)

    market = "KRW-BTC"

    # 동일한 조건으로 여러 번 계산하여 일관성 확인
    print("🔍 동일 조건 반복 테스트:")
    results = []

    for i in range(3):
        result = calculate_investment_return(market, 7, 1000000)
        if result['success']:
            results.append(result['return_rate'])
            print(f"   시도 {i+1}: {result['return_rate']:.4f}%")
        else:
            print(f"   시도 {i+1}: 실패")

    if len(results) > 1:
        # 모든 결과가 동일한지 확인
        all_same = all(abs(r - results[0]) < 0.001 for r in results)
        print(f"   일관성: {'✅ 통과' if all_same else '❌ 실패'}")


def run_all_tests():
    """모든 테스트 실행"""
    print("🧪 수익률 계산기 테스트 시작")
    print("=" * 60)

    test_annual_return_calculation()
    test_api_connections()
    test_investment_date_price_extraction()
    test_investment_calculation()
    test_edge_cases()
    test_calculation_accuracy()
    test_data_consistency()

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("\n💡 참고: 실제 투자 결과는 수수료, 세금 등을 고려하지 않은")
    print("   단순 계산 결과입니다. 실제 투자시 참고용으로만 활용하세요.")


if __name__ == "__main__":
    run_all_tests()
```

**작성 이유**:
- **계산 검증**: 수익률 계산 로직의 정확성을 다양한 방법으로 검증
- **데이터 무결성**: API에서 받은 데이터의 일관성과 유효성 확인
- **경계값 테스트**: 극단적인 입력값에서의 안정성 검증
- **실제 시나리오**: 현실적인 투자 상황을 시뮬레이션하여 실용성 확인
- **오류 처리**: 다양한 예외 상황에서의 적절한 대응 검증

---

## 🔧 구현 단계별 설명

### 1단계: 과거 데이터 수집 시스템
- **목적**: 업비트 API에서 일봉 데이터를 안정적으로 수집
- **구현**: `get_historical_data_api()` - 에러 처리와 데이터 검증 포함
- **핵심**: 투자 시점의 정확한 가격 정보 확보

### 2단계: 날짜 매칭 및 가격 추출
- **목적**: 지정한 일수 전의 정확한 가격 데이터 추출
- **구현**: `find_investment_date_price()` - 인덱스 계산과 데이터 파싱
- **주의사항**: 업비트 API는 최신순 정렬이므로 인덱스 주의

### 3단계: 투자 수익률 계산 엔진
- **목적**: 정확한 수익률과 관련 지표 계산
- **구현**:
  - 구매 수량 = 투자금액 ÷ 투자시점가격
  - 현재 가치 = 구매수량 × 현재가격
  - 수익률 = (현재가치 - 투자금액) ÷ 투자금액 × 100
- **추가**: 연간 복리 수익률로 투자 성과의 연간 기준 평가

### 4단계: 다중 시나리오 비교 시스템
- **목적**: 여러 투자 전략을 동시에 분석하여 최적 전략 도출
- **구현**: `compare_multiple_scenarios()` - 테이블 형태 비교 및 통계
- **인사이트**: 포트폴리오 다각화 효과와 최적 투자 시점 분석

### 5단계: 사용자 인터페이스 및 결과 해석
- **목적**: 복잡한 투자 지표를 일반인도 이해할 수 있게 표현
- **구현**:
  - 단계별 입력 가이드
  - 직관적인 결과 표시
  - 수익률에 따른 정성적 평가
- **사용성**: 프리셋 시나리오로 빠른 체험 가능

---

## 📋 Phase 4 실행 순서

1. **수익률 계산기 파일 생성**
   ```bash
   # src/return_calculator.py 파일 생성 및 코드 작성
   ```

2. **테스트 파일 생성**
   ```bash
   # tests/test_return_calculator.py 파일 생성 및 코드 작성
   ```

3. **기능 테스트 실행**
   ```bash
   python tests/test_return_calculator.py
   ```

4. **단독 실행 테스트**
   ```bash
   python src/return_calculator.py
   ```

5. **메인 프로그램에 연결**
   ```bash
   # main.py 파일 수정하여 Phase 4 기능 활성화
   ```

6. **통합 테스트**
   ```bash
   python main.py
   # 메뉴에서 3번 선택하여 수익률 계산기 실행
   ```

---

## 🎯 Phase 4 학습 목표 달성 확인

### seedprompt.md 요구사항 매칭:

1. **✅ 투자 시점과 투자 금액 설정**
   - `get_user_investment_settings()`: 사용자 입력
   - `get_preset_investment_scenarios()`: 프리셋 시나리오

2. **✅ 해당 시점의 가격과 현재 가격 비교**
   - `find_investment_date_price()`: 과거 가격 추출
   - `get_single_price_api()`: 현재가 조회
   - 가격 변화율 계산 및 표시

3. **✅ 수익률과 수익금 계산**
   - 정확한 수익률 계산 (현재가치 - 투자금액) ÷ 투자금액
   - 절대 수익금 계산
   - 연간 복리 수익률 계산

### 추가 구현된 고급 기능:
- **다중 시나리오 비교**: 여러 투자 전략 동시 분석
- **투자 성과 평가**: 수익률 구간별 정성적 평가
- **연간 수익률**: 복리 기준 연간 수익률로 표준화된 비교
- **포트폴리오 분석**: 여러 암호화폐 투자 결과 종합
- **데이터 검증**: 과거 데이터의 무결성과 일관성 검증

---

## 💡 투자 분석 활용 가이드

### 수익률 해석 방법:
- **10% 미만**: 안정적이지만 보통 수준의 수익
- **10-20%**: 양호한 수익률
- **20% 이상**: 매우 높은 수익률 (리스크도 높았을 가능성)
- **마이너스**: 손실 - 투자 타이밍이나 종목 선택 재검토 필요

### 연간 수익률의 의미:
- **장기 투자 기준**: 연 10-15%면 우수한 수익률
- **단기 고수익**: 짧은 기간의 높은 수익률은 지속가능성 검토 필요
- **변동성 고려**: 암호화폐는 변동성이 크므로 연간 수익률을 참고지표로 활용

### 다중 시나리오 비교 활용:
- **분산투자 효과**: 여러 암호화폐에 투자했을 때의 리스크 분산 확인
- **타이밍 분석**: 같은 종목이라도 투자 시점에 따른 결과 차이 분석
- **포트폴리오 최적화**: 최고 수익률 종목과 시점 조합 발견

---

## 📌 Phase 4 완료 후 확인사항

- [ ] 수익률 계산기가 정상적으로 실행되는가?
- [ ] 단일 시나리오 계산이 정확한가?
- [ ] 프리셋 시나리오 비교가 올바르게 동작하는가?
- [ ] 사용자 직접 입력이 편리하고 안정적인가?
- [ ] 다중 시나리오 비교 테이블이 명확한가?
- [ ] 투자 성과 평가 메시지가 적절한가?
- [ ] 연간 수익률 계산이 정확한가?
- [ ] 모든 경계값 테스트가 통과하는가?
- [ ] API 오류 상황에서 안정적인가?

---

## 🏆 전체 프로젝트 완성

Phase 4가 완료되면 암호화폐 분석 프로젝트의 모든 기능이 구현됩니다:

1. **Phase 1**: 견고한 프로젝트 기반 구조
2. **Phase 2**: 포트폴리오 분석으로 현재 보유 현황 파악
3. **Phase 3**: 가격 알림으로 실시간 모니터링
4. **Phase 4**: 수익률 계산으로 투자 성과 분석

이제 실제 암호화폐 투자와 관리에 활용할 수 있는 완전한 도구가 완성됩니다!