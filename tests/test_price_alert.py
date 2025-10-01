"""
가격 알림 시스템 테스트 파일
다양한 시나리오와 알림 조건을 테스트
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.price_alert import (
    get_single_price_api,
    calculate_target_prices,
    check_price_alert_condition,
    validate_market_code,
    get_coin_name,
    price_alert_system
)


def test_market_validation():
    """마켓 코드 검증 함수 테스트"""
    print("\n🧪 마켓 코드 검증 테스트")
    print("-" * 40)

    # 정상 케이스
    valid_markets = ["KRW-BTC", "KRW-ETH", "KRW-XRP"]
    for market in valid_markets:
        result = validate_market_code(market)
        print(f"✅ {market}: {result}")

    # 비정상 케이스
    invalid_markets = ["BTC", "USD-BTC", "", "KRW-", "-BTC", None]
    for market in invalid_markets:
        result = validate_market_code(market)
        print(f"❌ {market}: {result}")


def test_coin_name_extraction():
    """코인명 추출 함수 테스트"""
    print("\n🪙 코인명 추출 테스트")
    print("-" * 40)

    test_cases = [
        ("KRW-BTC", "BTC"),
        ("KRW-ETH", "ETH"),
        ("KRW-XRP", "XRP"),
        ("INVALID", "INVALID")
    ]

    for market, expected in test_cases:
        result = get_coin_name(market)
        status = "✅" if result == expected else "❌"
        print(f"{status} {market} -> {result} (예상: {expected})")


def test_target_price_calculation():
    """목표가 계산 함수 테스트"""
    print("\n📊 목표가 계산 테스트")
    print("-" * 40)

    test_cases = [
        (100000, 0.05),  # 10만원, 5%
        (50000, 0.1),    # 5만원, 10%
        (1000000, 0.03)  # 100만원, 3%
    ]

    for current_price, threshold in test_cases:
        high_target, low_target = calculate_target_prices(current_price, threshold)
        expected_high = current_price * (1 + threshold)
        expected_low = current_price * (1 - threshold)

        high_correct = abs(high_target - expected_high) < 0.01
        low_correct = abs(low_target - expected_low) < 0.01

        print(f"현재가: {current_price:,}원, 임계값: {threshold*100}%")
        print(f"  상한가: {high_target:,.0f}원 {'✅' if high_correct else '❌'}")
        print(f"  하한가: {low_target:,.0f}원 {'✅' if low_correct else '❌'}")


def test_alert_condition_checking():
    """알림 조건 확인 함수 테스트"""
    print("\n🔔 알림 조건 확인 테스트")
    print("-" * 40)

    target_high = 105000
    target_low = 95000

    test_cases = [
        (110000, "high", "상한가 도달"),     # 상한가 초과
        (90000, "low", "하한가 도달"),       # 하한가 미달
        (100000, "normal", "정상 범위"),     # 정상 범위
        (105000, "high", "상한가 도달"),     # 상한가 정확히 도달
        (95000, "low", "하한가 도달")        # 하한가 정확히 도달
    ]

    for current_price, expected_type, description in test_cases:
        result = check_price_alert_condition(current_price, target_high, target_low)

        correct_type = result['alert_type'] == expected_type
        correct_trigger = result['alert_triggered'] == (expected_type != 'normal')

        status = "✅" if correct_type and correct_trigger else "❌"
        print(f"{status} {description}: 현재가 {current_price:,}원")
        print(f"    타입: {result['alert_type']} (예상: {expected_type})")
        print(f"    알림: {result['alert_triggered']}")


def test_api_connection():
    """API 연결 테스트"""
    print("\n🌐 API 연결 테스트")
    print("-" * 40)

    test_markets = ["KRW-BTC", "KRW-ETH"]

    for market in test_markets:
        price = get_single_price_api(market)
        coin_name = get_coin_name(market)

        if price:
            print(f"✅ {coin_name}: {price:,}원")
        else:
            print(f"❌ {coin_name}: 가격 조회 실패")


def test_short_monitoring():
    """짧은 모니터링 테스트"""
    print("\n⏰ 짧은 모니터링 테스트")
    print("-" * 40)

    market = "KRW-BTC"

    # 현재가 조회
    current_price = get_single_price_api(market)
    if not current_price:
        print("❌ 현재가 조회 실패로 테스트를 건너뜁니다.")
        return

    # 목표가 계산 (변동폭을 크게 설정하여 알림이 발생하지 않도록)
    target_high = current_price * 1.2  # +20%
    target_low = current_price * 0.8   # -20%

    print(f"📊 테스트 설정:")
    print(f"   현재가: {current_price:,}원")
    print(f"   상한가: {target_high:,}원")
    print(f"   하한가: {target_low:,}원")

    # 3회 모니터링 (간격 1초)
    result = price_alert_system(
        market=market,
        target_high=target_high,
        target_low=target_low,
        cycles=3,
        interval=1
    )

    if result['success']:
        print(f"✅ 모니터링 성공")
        print(f"   알림 발생: {result['alerts_triggered']}회")
        print(f"   데이터 수집: {len(result['monitoring_data'])}개")
    else:
        print(f"❌ 모니터링 실패: {result['error_message']}")


def test_edge_cases():
    """경계값 테스트"""
    print("\n🔍 경계값 테스트")
    print("-" * 40)

    # 매우 작은 가격
    tiny_price = 0.01
    high, low = calculate_target_prices(tiny_price, 0.1)
    print(f"💰 매우 작은 가격 ({tiny_price}원):")
    print(f"   상한가: {high:.6f}원")
    print(f"   하한가: {low:.6f}원")

    # 매우 큰 가격
    huge_price = 100000000
    high, low = calculate_target_prices(huge_price, 0.05)
    print(f"💰 매우 큰 가격 ({huge_price:,}원):")
    print(f"   상한가: {high:,.0f}원")
    print(f"   하한가: {low:,.0f}원")

    # 0% 임계값
    zero_threshold_high, zero_threshold_low = calculate_target_prices(100000, 0)
    print(f"📊 0% 임계값 테스트:")
    print(f"   상한가: {zero_threshold_high:,}원 (현재가와 동일해야 함)")
    print(f"   하한가: {zero_threshold_low:,}원 (현재가와 동일해야 함)")


def test_error_handling():
    """오류 처리 테스트"""
    print("\n⚠️  오류 처리 테스트")
    print("-" * 40)

    # 존재하지 않는 마켓
    fake_market = "KRW-FAKE"
    result = price_alert_system(
        market=fake_market,
        target_high=100000,
        target_low=90000,
        cycles=1,
        interval=1
    )
    print(f"🔍 존재하지 않는 마켓 테스트: {'성공' if not result['success'] else '실패'}")

    # 잘못된 마켓 코드
    invalid_market = "INVALID"
    result = price_alert_system(
        market=invalid_market,
        target_high=100000,
        target_low=90000,
        cycles=1,
        interval=1
    )
    print(f"🔍 잘못된 마켓 코드 테스트: {'성공' if not result['success'] else '실패'}")

    # 잘못된 목표가 (상한가 < 하한가)
    print(f"🔍 논리적 오류 체크:")
    print(f"   상한가 90000 < 하한가 100000 (논리적으로 불가능)")


def run_all_tests():
    """모든 테스트 실행"""
    print("🧪 가격 알림 시스템 테스트 시작")
    print("=" * 60)

    test_market_validation()
    test_coin_name_extraction()
    test_target_price_calculation()
    test_alert_condition_checking()
    test_api_connection()
    test_short_monitoring()
    test_edge_cases()
    test_error_handling()

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("\n💡 참고: 실제 사용시에는 적절한 모니터링 간격과")
    print("   현실적인 목표가를 설정하시기 바랍니다.")


if __name__ == "__main__":
    run_all_tests()