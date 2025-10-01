"""
업비트 API 클라이언트 유틸리티
모든 API 호출을 담당하는 공통 함수들
"""

import requests
import time
from typing import List, Dict, Any, Optional
from config.settings import API_ENDPOINTS, REQUEST_TIMEOUT, MAX_RETRIES


def make_api_request(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
    """
    API 요청을 수행하는 기본 함수

    Args:
        url (str): 요청할 API URL
        params (dict, optional): 요청 파라미터

    Returns:
        dict: API 응답 데이터 (JSON)
        None: 요청 실패시
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # HTTP 에러 체크
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 실패 (시도 {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)  # 1초 대기 후 재시도
            else:
                print("API 요청을 포기합니다.")
                return None


def get_current_prices(markets: List[str]) -> Dict[str, float]:
    """
    여러 암호화폐의 현재가를 조회하는 함수
    일부 마켓이 실패해도 성공한 마켓들의 가격은 반환

    Args:
        markets (List[str]): 조회할 마켓 코드 리스트 (예: ['KRW-BTC', 'KRW-ETH'])

    Returns:
        Dict[str, float]: 마켓별 현재가 딕셔너리
    """
    if not markets:
        return {}

    # 단일 마켓인 경우 개별 조회 사용
    if len(markets) == 1:
        price = get_single_price(markets[0])
        return {markets[0]: price} if price is not None else {}

    # 먼저 일괄 조회 시도
    markets_str = ','.join(markets)
    url = API_ENDPOINTS["ticker"]
    params = {"markets": markets_str}

    response_data = make_api_request(url, params)

    prices = {}
    if response_data:
        # 성공한 마켓들 처리
        for data in response_data:
            market = data.get('market')
            price = data.get('trade_price')
            if market and price:
                prices[market] = float(price)
    
    # 일괄 조회가 실패했거나 일부 마켓이 누락된 경우 개별 조회 시도
    missing_markets = [market for market in markets if market not in prices]
    if missing_markets:
        if not response_data:
            # 일괄 조회가 완전히 실패한 경우 (존재하지 않는 마켓 포함)
            print(f"⚠️  일괄 조회 실패, 모든 마켓을 개별 조회합니다")
            for market in markets:
                individual_price = get_single_price(market)
                if individual_price is not None:
                    prices[market] = individual_price
                    print(f"   ✅ {market}: {individual_price:,}원")
                else:
                    print(f"   ❌ {market}: 마켓이 존재하지 않습니다")
        else:
            # 일부 마켓만 누락된 경우
            print(f"⚠️  일부 마켓 조회 실패, 개별 조회 시도: {', '.join(missing_markets)}")
            for market in missing_markets:
                individual_price = get_single_price(market)
                if individual_price is not None:
                    prices[market] = individual_price
                    print(f"   ✅ {market}: {individual_price:,}원")
                else:
                    print(f"   ❌ {market}: 마켓이 존재하지 않습니다")

    return prices


def get_single_price(market: str) -> Optional[float]:
    """
    단일 암호화폐의 현재가를 조회하는 함수

    Args:
        market (str): 조회할 마켓 코드 (예: 'KRW-BTC')

    Returns:
        float: 현재가
        None: 조회 실패시
    """
    url = API_ENDPOINTS["ticker"]
    params = {"markets": market}

    response_data = make_api_request(url, params)

    if not response_data or len(response_data) == 0:
        return None

    return float(response_data[0].get('trade_price', 0))


def get_historical_data(market: str, count: int) -> Optional[List[Dict]]:
    """
    암호화폐의 과거 일봉 데이터를 조회하는 함수

    Args:
        market (str): 마켓 코드 (예: 'KRW-BTC')
        count (int): 조회할 일수

    Returns:
        List[Dict]: 일봉 데이터 리스트 (최신순)
        None: 조회 실패시
    """
    url = API_ENDPOINTS["candles_days"]
    params = {
        "market": market,
        "count": count
    }

    response_data = make_api_request(url, params)

    if not response_data:
        return None

    return response_data