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

    Args:
        markets (List[str]): 조회할 마켓 코드 리스트 (예: ['KRW-BTC', 'KRW-ETH'])

    Returns:
        Dict[str, float]: 마켓별 현재가 딕셔너리
    """
    if not markets:
        return {}

    markets_str = ','.join(markets)
    url = API_ENDPOINTS["ticker"]
    params = {"markets": markets_str}

    response_data = make_api_request(url, params)

    if not response_data:
        return {}

    prices = {}
    for data in response_data:
        market = data.get('market')
        price = data.get('trade_price')
        if market and price:
            prices[market] = float(price)

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