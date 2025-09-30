# Phase 2: 암호화폐 포트폴리오 분석기 구현

## 📋 진행 체크리스트

### 1. 포트폴리오 데이터 구조 설계
- [ ] 포트폴리오 딕셔너리 구조 정의
- [ ] 분석 결과 데이터 구조 설계
- [ ] 입력 데이터 검증 로직 구현

### 2. API 연동 함수 구현
- [ ] 현재가 조회 함수 구현 (`get_current_prices_api`)
- [ ] API 응답 데이터 파싱 로직 구현
- [ ] 에러 처리 및 예외 상황 대응

### 3. 포트폴리오 분석 로직 구현
- [ ] 개별 암호화폐 가치 계산
- [ ] 전체 포트폴리오 가치 계산
- [ ] 비중 계산 및 포맷팅
- [ ] 분석 결과 정리

### 4. 출력 및 표시 기능 구현
- [ ] 테이블 형태 결과 출력
- [ ] 요약 정보 출력
- [ ] 사용자 인터페이스 구현

### 5. 테스트 및 검증
- [ ] 샘플 포트폴리오로 기능 테스트
- [ ] API 오류 상황 테스트
- [ ] 경계값 테스트 (0원, 소수점 등)

---

## 📁 생성할 파일

### 1. src/portfolio_analyzer.py (메인 구현 파일)
### 2. tests/test_portfolio_analyzer.py (테스트 파일)

---

## 📝 상세 구현 계획

### 1. src/portfolio_analyzer.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/src/portfolio_analyzer.py`

**파일 내용**:
```python
"""
암호화폐 포트폴리오 분석기
사용자의 암호화폐 보유 현황을 분석하여 총 가치, 개별 가치, 비중 등을 계산
"""

from typing import Dict, List, Any
from utils.api_client import get_current_prices
from utils.format_utils import (
    format_currency,
    format_percentage,
    format_crypto_amount,
    create_table_header,
    create_table_row
)
from config.settings import DEFAULT_CRYPTOS


def get_current_prices_api(markets: List[str]) -> Dict[str, float]:
    """
    업비트 API를 통해 현재가를 조회하는 함수

    Args:
        markets (List[str]): 조회할 마켓 코드 리스트 ['KRW-BTC', 'KRW-ETH']

    Returns:
        Dict[str, float]: 마켓별 현재가 딕셔너리
    """
    print(f"📡 {len(markets)}개 암호화폐의 현재가를 조회 중...")

    try:
        prices = get_current_prices(markets)

        if not prices:
            print("❌ 현재가 조회에 실패했습니다.")
            return {}

        print(f"✅ {len(prices)}개 암호화폐의 현재가 조회 완료")
        return prices

    except Exception as e:
        print(f"❌ API 호출 중 오류 발생: {e}")
        return {}


def validate_portfolio(portfolio: Dict[str, float]) -> bool:
    """
    포트폴리오 데이터 유효성 검증

    Args:
        portfolio (Dict[str, float]): 포트폴리오 딕셔너리

    Returns:
        bool: 유효성 검증 결과
    """
    if not portfolio:
        print("❌ 포트폴리오가 비어있습니다.")
        return False

    for market, quantity in portfolio.items():
        if not isinstance(market, str) or not market:
            print(f"❌ 잘못된 마켓 코드: {market}")
            return False

        if not isinstance(quantity, (int, float)) or quantity <= 0:
            print(f"❌ 잘못된 수량: {market} = {quantity}")
            return False

        if not market.startswith('KRW-'):
            print(f"❌ 지원하지 않는 마켓: {market} (KRW 마켓만 지원)")
            return False

    return True


def analyze_portfolio(portfolio: Dict[str, float]) -> Dict[str, Any]:
    """
    포트폴리오를 분석하여 각 암호화폐의 가치와 비중을 계산

    Args:
        portfolio (Dict[str, float]): 포트폴리오 딕셔너리
                                     예: {'KRW-BTC': 0.1, 'KRW-ETH': 2.5}

    Returns:
        Dict[str, Any]: 분석 결과
        {
            'total_value': float,           # 총 포트폴리오 가치
            'analysis': List[Dict],         # 개별 분석 결과
            'success': bool,                # 분석 성공 여부
            'error_message': str            # 오류 메시지 (실패시)
        }
    """
    print("\n🔍 포트폴리오 분석을 시작합니다...")

    # 1. 입력 데이터 검증
    if not validate_portfolio(portfolio):
        return {
            'success': False,
            'error_message': '포트폴리오 데이터가 유효하지 않습니다.',
            'total_value': 0,
            'analysis': []
        }

    # 2. 현재가 조회
    markets = list(portfolio.keys())
    current_prices = get_current_prices_api(markets)

    if not current_prices:
        return {
            'success': False,
            'error_message': '현재가 조회에 실패했습니다.',
            'total_value': 0,
            'analysis': []
        }

    # 3. 각 암호화폐별 분석
    portfolio_analysis = []
    total_value = 0

    print("\n📊 개별 암호화폐 분석 중...")

    for market, quantity in portfolio.items():
        if market not in current_prices:
            print(f"⚠️  {market}의 현재가를 찾을 수 없어 건너뜁니다.")
            continue

        current_price = current_prices[market]
        individual_value = current_price * quantity
        total_value += individual_value

        # 코인명 추출 (KRW-BTC -> BTC)
        coin_name = market.split('-')[1]

        analysis_item = {
            'market': market,
            'coin_name': coin_name,
            'quantity': quantity,
            'current_price': current_price,
            'value': individual_value,
            'percentage': 0  # 비중은 나중에 계산
        }

        portfolio_analysis.append(analysis_item)
        print(f"   {coin_name}: {format_crypto_amount(quantity)} x {format_currency(current_price)} = {format_currency(individual_value)}")

    # 4. 비중 계산
    if total_value > 0:
        for item in portfolio_analysis:
            item['percentage'] = (item['value'] / total_value) * 100

    print(f"\n💰 총 포트폴리오 가치: {format_currency(total_value)}")

    return {
        'success': True,
        'error_message': '',
        'total_value': total_value,
        'analysis': portfolio_analysis
    }


def print_portfolio_summary(analysis_result: Dict[str, Any]) -> None:
    """
    포트폴리오 분석 결과를 요약하여 출력

    Args:
        analysis_result (Dict): analyze_portfolio 함수의 결과
    """
    if not analysis_result['success']:
        print(f"\n❌ 분석 실패: {analysis_result['error_message']}")
        return

    total_value = analysis_result['total_value']
    analysis = analysis_result['analysis']

    print(f"\n" + "="*60)
    print(f"📊 포트폴리오 분석 결과 요약")
    print(f"="*60)
    print(f"💰 총 포트폴리오 가치: {format_currency(total_value)}")
    print(f"🪙 보유 암호화폐 수: {len(analysis)}개")

    if analysis:
        # 가장 비중이 높은 암호화폐 찾기
        max_holding = max(analysis, key=lambda x: x['percentage'])
        print(f"📈 최대 보유: {max_holding['coin_name']} ({format_percentage(max_holding['percentage'])})")

        # 가장 비중이 낮은 암호화폐 찾기
        min_holding = min(analysis, key=lambda x: x['percentage'])
        print(f"📉 최소 보유: {min_holding['coin_name']} ({format_percentage(min_holding['percentage'])})")


def print_portfolio_table(analysis_result: Dict[str, Any]) -> None:
    """
    포트폴리오 분석 결과를 테이블 형태로 출력

    Args:
        analysis_result (Dict): analyze_portfolio 함수의 결과
    """
    if not analysis_result['success']:
        return

    analysis = analysis_result['analysis']

    if not analysis:
        print("\n❌ 출력할 데이터가 없습니다.")
        return

    print(f"\n📋 상세 분석 결과")
    print(f"-"*80)

    # 테이블 헤더 설정
    columns = ['암호화폐', '보유수량', '현재가', '보유가치', '비중']
    widths = [10, 15, 15, 15, 10]
    alignments = ['center', 'right', 'right', 'right', 'center']

    # 헤더 출력
    print(create_table_header(columns, widths))

    # 비중순으로 정렬 (높은 순)
    sorted_analysis = sorted(analysis, key=lambda x: x['percentage'], reverse=True)

    # 각 행 출력
    for item in sorted_analysis:
        values = [
            item['coin_name'],
            format_crypto_amount(item['quantity']),
            format_currency(item['current_price']),
            format_currency(item['value']),
            format_percentage(item['percentage'])
        ]
        print(create_table_row(values, widths, alignments))

    # 총합 행 추가
    print("|" + "-"*78 + "|")
    total_row = [
        "총합",
        "-",
        "-",
        format_currency(analysis_result['total_value']),
        "100.00%"
    ]
    print(create_table_row(total_row, widths, alignments))


def get_sample_portfolio() -> Dict[str, float]:
    """
    샘플 포트폴리오를 반환 (테스트용)

    Returns:
        Dict[str, float]: 샘플 포트폴리오
    """
    return {
        "KRW-BTC": 0.05,      # 비트코인 0.05개
        "KRW-ETH": 1.2,       # 이더리움 1.2개
        "KRW-XRP": 500,       # 리플 500개
        "KRW-ADA": 1000       # 에이다 1000개
    }


def get_custom_portfolio() -> Dict[str, float]:
    """
    사용자로부터 포트폴리오 입력받기

    Returns:
        Dict[str, float]: 사용자 입력 포트폴리오
    """
    print("\n📝 포트폴리오를 입력해주세요")
    print("형식: 마켓코드 수량 (예: KRW-BTC 0.1)")
    print("입력 완료시 'done' 입력")
    print("-" * 40)

    portfolio = {}

    while True:
        try:
            user_input = input("입력 (마켓코드 수량 또는 'done'): ").strip()

            if user_input.lower() == 'done':
                break

            if not user_input:
                continue

            parts = user_input.split()
            if len(parts) != 2:
                print("❌ 형식이 잘못되었습니다. '마켓코드 수량' 형식으로 입력하세요.")
                continue

            market = parts[0].upper()
            quantity = float(parts[1])

            if not market.startswith('KRW-'):
                print("❌ KRW 마켓만 지원합니다. (예: KRW-BTC)")
                continue

            if quantity <= 0:
                print("❌ 수량은 0보다 커야 합니다.")
                continue

            portfolio[market] = quantity
            print(f"✅ 추가됨: {market} {quantity}")

        except ValueError:
            print("❌ 수량은 숫자여야 합니다.")
        except KeyboardInterrupt:
            print("\n❌ 입력이 취소되었습니다.")
            return {}

    return portfolio


def run_portfolio_analyzer():
    """
    포트폴리오 분석기 메인 실행 함수
    """
    print("\n" + "="*60)
    print("📊 암호화폐 포트폴리오 분석기")
    print("="*60)

    # 포트폴리오 선택
    print("\n포트폴리오를 선택하세요:")
    print("1. 샘플 포트폴리오 사용")
    print("2. 직접 입력")

    try:
        choice = input("선택 (1-2): ").strip()

        if choice == '1':
            portfolio = get_sample_portfolio()
            print(f"\n📋 샘플 포트폴리오 사용:")
            for market, quantity in portfolio.items():
                coin_name = market.split('-')[1]
                print(f"   {coin_name}: {format_crypto_amount(quantity)}")

        elif choice == '2':
            portfolio = get_custom_portfolio()
            if not portfolio:
                print("❌ 포트폴리오가 입력되지 않았습니다.")
                return

        else:
            print("❌ 잘못된 선택입니다.")
            return

        # 포트폴리오 분석 실행
        result = analyze_portfolio(portfolio)

        # 결과 출력
        print_portfolio_summary(result)
        print_portfolio_table(result)

        print(f"\n" + "="*60)
        print("✅ 포트폴리오 분석이 완료되었습니다!")

    except KeyboardInterrupt:
        print("\n❌ 분석이 취소되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    # 직접 실행시 테스트
    run_portfolio_analyzer()
```

**작성 이유**:
- **모듈화된 함수 구조**: 각 기능을 독립적인 함수로 분리하여 테스트와 유지보수 용이
- **에러 처리**: API 호출 실패, 잘못된 입력 등 다양한 예외 상황 대응
- **데이터 검증**: 포트폴리오 입력값의 유효성을 사전에 검증
- **유연한 입력**: 샘플 데이터와 사용자 직접 입력 모두 지원
- **명확한 출력**: 요약 정보와 상세 테이블을 통한 이해하기 쉬운 결과 표시
- **타입 힌트**: 함수의 입력/출력 타입을 명시하여 코드 안정성 향상

### 2. tests/test_portfolio_analyzer.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/tests/test_portfolio_analyzer.py`

**파일 내용**:
```python
"""
포트폴리오 분석기 테스트 파일
다양한 시나리오와 경계값을 테스트
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.portfolio_analyzer import (
    analyze_portfolio,
    validate_portfolio,
    get_current_prices_api,
    get_sample_portfolio
)


def test_validate_portfolio():
    """포트폴리오 검증 함수 테스트"""
    print("\n🧪 포트폴리오 검증 테스트")
    print("-" * 40)

    # 정상 케이스
    valid_portfolio = {"KRW-BTC": 0.1, "KRW-ETH": 2.5}
    result = validate_portfolio(valid_portfolio)
    print(f"✅ 정상 포트폴리오 검증: {result}")

    # 빈 포트폴리오
    empty_portfolio = {}
    result = validate_portfolio(empty_portfolio)
    print(f"❌ 빈 포트폴리오 검증: {result}")

    # 잘못된 수량
    invalid_quantity = {"KRW-BTC": -0.1}
    result = validate_portfolio(invalid_quantity)
    print(f"❌ 음수 수량 검증: {result}")

    # 잘못된 마켓 코드
    invalid_market = {"USD-BTC": 0.1}
    result = validate_portfolio(invalid_market)
    print(f"❌ 잘못된 마켓 검증: {result}")


def test_api_connection():
    """API 연결 테스트"""
    print("\n🌐 API 연결 테스트")
    print("-" * 40)

    test_markets = ["KRW-BTC", "KRW-ETH"]
    prices = get_current_prices_api(test_markets)

    if prices:
        print(f"✅ API 연결 성공: {len(prices)}개 가격 조회")
        for market, price in prices.items():
            print(f"   {market}: {price:,}원")
    else:
        print("❌ API 연결 실패")


def test_portfolio_analysis():
    """포트폴리오 분석 테스트"""
    print("\n📊 포트폴리오 분석 테스트")
    print("-" * 40)

    # 샘플 포트폴리오로 테스트
    sample_portfolio = get_sample_portfolio()
    print(f"📋 테스트 포트폴리오: {sample_portfolio}")

    result = analyze_portfolio(sample_portfolio)

    if result['success']:
        print(f"✅ 분석 성공")
        print(f"   총 가치: {result['total_value']:,}원")
        print(f"   분석 항목 수: {len(result['analysis'])}개")

        # 비중 합계 확인 (100%에 가까워야 함)
        total_percentage = sum(item['percentage'] for item in result['analysis'])
        print(f"   비중 합계: {total_percentage:.2f}%")

        if abs(total_percentage - 100) < 0.01:
            print("✅ 비중 계산 정확")
        else:
            print("❌ 비중 계산 오류")

    else:
        print(f"❌ 분석 실패: {result['error_message']}")


def test_edge_cases():
    """경계값 테스트"""
    print("\n🔍 경계값 테스트")
    print("-" * 40)

    # 매우 작은 수량
    tiny_portfolio = {"KRW-BTC": 0.00000001}
    result = analyze_portfolio(tiny_portfolio)
    print(f"💰 매우 작은 수량 테스트: {'성공' if result['success'] else '실패'}")

    # 매우 큰 수량
    large_portfolio = {"KRW-BTC": 1000000}
    result = analyze_portfolio(large_portfolio)
    print(f"💰 매우 큰 수량 테스트: {'성공' if result['success'] else '실패'}")

    # 단일 코인
    single_portfolio = {"KRW-BTC": 1.0}
    result = analyze_portfolio(single_portfolio)
    if result['success'] and len(result['analysis']) > 0:
        percentage = result['analysis'][0]['percentage']
        print(f"🪙 단일 코인 비중: {percentage:.2f}% ({'정확' if abs(percentage - 100) < 0.01 else '오류'})")


def test_error_handling():
    """오류 처리 테스트"""
    print("\n⚠️  오류 처리 테스트")
    print("-" * 40)

    # 존재하지 않는 마켓
    fake_portfolio = {"KRW-FAKE": 1.0}
    result = analyze_portfolio(fake_portfolio)
    print(f"🔍 존재하지 않는 마켓: {'성공' if result['success'] else '실패'}")

    # 잘못된 타입
    try:
        invalid_type_portfolio = {"KRW-BTC": "not_a_number"}
        result = validate_portfolio(invalid_type_portfolio)
        print(f"🔍 잘못된 타입 처리: {'성공' if not result else '실패'}")
    except Exception as e:
        print(f"🔍 예외 발생 (예상됨): {type(e).__name__}")


def run_all_tests():
    """모든 테스트 실행"""
    print("🧪 포트폴리오 분석기 테스트 시작")
    print("=" * 60)

    test_validate_portfolio()
    test_api_connection()
    test_portfolio_analysis()
    test_edge_cases()
    test_error_handling()

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")


if __name__ == "__main__":
    run_all_tests()
```

**작성 이유**:
- **포괄적 테스트**: 정상 케이스부터 예외 상황까지 다양한 시나리오 검증
- **경계값 테스트**: 매우 작은/큰 수량, 단일 코인 등 극단적 상황 테스트
- **에러 처리 검증**: 잘못된 입력과 API 오류 상황에 대한 대응 확인
- **자동화된 검증**: 비중 계산의 정확성 등을 자동으로 확인
- **독립적 테스트**: 각 기능을 개별적으로 테스트할 수 있도록 구성

---

## 🔧 구현 단계별 설명

### 1단계: 포트폴리오 정의 및 검증
- **목적**: 사용자 입력의 유효성을 보장하여 런타임 오류 방지
- **구현**: `validate_portfolio()` 함수에서 마켓 코드 형식, 수량 범위 등 체크
- **중요성**: 잘못된 데이터로 인한 API 호출 실패나 계산 오류를 사전에 방지

### 2단계: API 호출 및 현재가 조회
- **목적**: 업비트 API에서 실시간 암호화폐 가격 정보 획득
- **구현**: `get_current_prices_api()` 함수에서 여러 마켓의 가격을 한 번에 조회
- **최적화**: 개별 호출 대신 배치 호출로 API 효율성 향상

### 3단계: 포트폴리오 분석 로직
- **목적**: 각 암호화폐의 가치와 전체 포트폴리오에서의 비중 계산
- **구현**:
  - 개별 가치 = 현재가 × 보유 수량
  - 총 가치 = 모든 개별 가치의 합
  - 비중 = (개별 가치 ÷ 총 가치) × 100
- **정확성**: 부동소수점 연산의 정밀도 고려

### 4단계: 결과 출력 및 포맷팅
- **목적**: 분석 결과를 사용자가 이해하기 쉬운 형태로 표시
- **구현**:
  - 요약 정보: 총 가치, 최대/최소 보유 코인
  - 상세 테이블: 각 코인별 상세 정보를 표 형태로 정리
- **사용성**: 비중 높은 순으로 정렬하여 중요 정보 우선 표시

---

## 📋 Phase 2 실행 순서

1. **포트폴리오 분석기 파일 생성**
   ```bash
   # src/portfolio_analyzer.py 파일 생성 및 코드 작성
   ```

2. **테스트 파일 생성**
   ```bash
   # tests/test_portfolio_analyzer.py 파일 생성 및 코드 작성
   ```

3. **기능 테스트 실행**
   ```bash
   python tests/test_portfolio_analyzer.py
   ```

4. **메인 프로그램에 연결**
   ```bash
   # main.py 파일에서 Phase 2 관련 주석 해제 및 import 추가
   ```

5. **통합 테스트**
   ```bash
   python main.py
   # 메뉴에서 1번 선택하여 포트폴리오 분석기 실행
   ```

---

## 🎯 Phase 2 학습 목표 달성 확인

### seedprompt.md 요구사항 매칭:

1. **✅ 보유 암호화폐와 수량을 딕셔너리로 정의**
   - `get_sample_portfolio()` 및 `get_custom_portfolio()` 함수로 구현

2. **✅ 각 암호화폐의 현재 가치 계산**
   - `analyze_portfolio()` 함수에서 현재가 × 수량으로 계산

3. **✅ 전체 포트폴리오 가치 계산**
   - 개별 가치들의 총합으로 계산

4. **✅ 각 암호화폐의 포트폴리오 내 비중 계산**
   - (개별 가치 ÷ 총 가치) × 100으로 비중 계산

### 추가 구현된 기능:
- **입력 검증**: 잘못된 포트폴리오 데이터 사전 체크
- **에러 처리**: API 실패, 네트워크 오류 등 예외 상황 대응
- **사용자 친화적 인터페이스**: 샘플/직접입력 선택, 테이블 형태 출력
- **포괄적 테스트**: 다양한 시나리오에 대한 자동화된 테스트

---

## 📌 Phase 2 완료 후 확인사항

- [ ] 포트폴리오 분석기가 정상적으로 실행되는가?
- [ ] 샘플 포트폴리오로 테스트가 성공하는가?
- [ ] 사용자 직접 입력이 올바르게 동작하는가?
- [ ] API 오류 상황에서 적절한 에러 메시지가 출력되는가?
- [ ] 테이블 출력이 깔끔하고 이해하기 쉬운가?
- [ ] 비중 계산이 정확한가? (총합 100%)
- [ ] 모든 테스트가 통과하는가?

Phase 2가 완료되면 Phase 3(가격 알림 시스템) 구현을 진행합니다.