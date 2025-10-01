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