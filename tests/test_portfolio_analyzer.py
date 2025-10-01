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
    expected = True
    status = "✅" if result == expected else "❌"
    print(f"{status} 정상 포트폴리오 검증: {result} (예상: {expected})")

    # 빈 포트폴리오 (유효하지 않음)
    empty_portfolio = {}
    result = validate_portfolio(empty_portfolio)
    expected = False
    status = "✅" if result == expected else "❌"
    print(f"{status} 빈 포트폴리오 검증: {result} (예상: {expected})")

    # 잘못된 수량 (음수) - 유효하지 않음
    invalid_quantity = {"KRW-BTC": -0.1}
    result = validate_portfolio(invalid_quantity)
    expected = False
    status = "✅" if result == expected else "❌"
    print(f"{status} 음수 수량 검증: {result} (예상: {expected})")
    
    # 0 수량 (이제 허용됨)
    zero_quantity = {"KRW-BTC": 0}
    result = validate_portfolio(zero_quantity)
    expected = True
    status = "✅" if result == expected else "❌"
    print(f"{status} 0 수량 검증: {result} (예상: {expected})")

    # 잘못된 마켓 코드 - 유효하지 않음
    invalid_market = {"USD-BTC": 0.1}
    result = validate_portfolio(invalid_market)
    expected = False
    status = "✅" if result == expected else "❌"
    print(f"{status} 잘못된 마켓 검증: {result} (예상: {expected})")


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

    # 존재하지 않는 마켓 (테스트용 - KRW-FAKE는 실제로 존재하지 않음)
    fake_portfolio = {"KRW-FAKE": 1.0}
    result = analyze_portfolio(fake_portfolio)
    if result['success']:
        print(f"🔍 존재하지 않는 마켓: 성공 (스킵된 마켓: {len(result.get('skipped_markets', []))}개)")
    else:
        print(f"🔍 존재하지 않는 마켓: 실패 - {result['error_message']}")
    
    # 혼합 포트폴리오 (정상 + 존재하지 않는 마켓)
    # KRW-BTC는 실제 마켓, KRW-FAKE는 테스트용 존재하지 않는 마켓
    mixed_portfolio = {"KRW-BTC": 0.1, "KRW-FAKE": 1.0}
    result = analyze_portfolio(mixed_portfolio)
    if result['success']:
        analyzed_count = len(result.get('analyzed_markets', []))
        skipped_count = len(result.get('skipped_markets', []))
        print(f"🔍 혼합 포트폴리오: 성공 (분석: {analyzed_count}개, 스킵: {skipped_count}개)")
    else:
        print(f"🔍 혼합 포트폴리오: 실패")
    
    # 실제 존재하는 마켓들로만 구성된 포트폴리오 테스트
    real_markets_portfolio = {"KRW-BTC": 0.05, "KRW-ETH": 0.1}
    result = analyze_portfolio(real_markets_portfolio)
    if result['success']:
        analyzed_count = len(result.get('analyzed_markets', []))
        print(f"🔍 실제 마켓만: 성공 (분석: {analyzed_count}개)")
    else:
        print(f"🔍 실제 마켓만: 실패")

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