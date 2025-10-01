"""
암호화폐 수익률 계산기
과거 특정 시점에 투자했다면 현재 수익률이 얼마인지 계산
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가 (직접 실행시)
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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