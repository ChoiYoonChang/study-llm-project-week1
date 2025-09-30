"""
API 클라이언트 기본 테스트
실제 API 호출 테스트 및 연결 확인
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_client import get_current_prices, get_single_price
from config.settings import DEFAULT_CRYPTOS


def test_api_connection():
    """API 연결 테스트"""
    print("🔍 API 연결 테스트를 시작합니다...")

    # 단일 코인 가격 조회 테스트
    print("\n1. 비트코인 현재가 조회 테스트")
    btc_price = get_single_price("KRW-BTC")
    if btc_price:
        print(f"✅ 성공: BTC 현재가 = {btc_price:,}원")
    else:
        print("❌ 실패: BTC 현재가 조회 실패")

    # 여러 코인 가격 조회 테스트
    print("\n2. 여러 코인 현재가 조회 테스트")
    test_markets = DEFAULT_CRYPTOS[:3]  # 처음 3개만 테스트
    prices = get_current_prices(test_markets)

    if prices:
        print("✅ 성공: 여러 코인 가격 조회")
        for market, price in prices.items():
            coin_name = market.split('-')[1]
            print(f"   {coin_name}: {price:,}원")
    else:
        print("❌ 실패: 여러 코인 가격 조회 실패")


def test_format_functions():
    """포맷팅 함수 테스트"""
    print("\n🎨 포맷팅 함수 테스트를 시작합니다...")

    from utils.format_utils import format_currency, format_percentage, format_crypto_amount

    # 통화 포맷팅 테스트
    test_amount = 1234567.89
    formatted = format_currency(test_amount)
    print(f"✅ 통화 포맷팅: {test_amount} → {formatted}")

    # 퍼센트 포맷팅 테스트
    test_percentage = 12.3456
    formatted_pct = format_percentage(test_percentage)
    print(f"✅ 퍼센트 포맷팅: {test_percentage} → {formatted_pct}")

    # 암호화폐 수량 포맷팅 테스트
    test_crypto = 0.00123456
    formatted_crypto = format_crypto_amount(test_crypto)
    print(f"✅ 암호화폐 포맷팅: {test_crypto} → {formatted_crypto}")


if __name__ == "__main__":
    print("🧪 Phase 1 기본 기능 테스트")
    print("=" * 50)

    test_api_connection()
    test_format_functions()

    print("\n" + "=" * 50)
    print("✅ Phase 1 테스트 완료!")