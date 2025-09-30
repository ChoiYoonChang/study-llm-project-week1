"""
pytest 설정 및 공통 fixture 정의
모든 테스트에서 공통으로 사용되는 설정과 데이터를 관리
"""
import os
import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from typing import Dict, List, Any

# 테스트 환경 설정
os.environ['TESTING'] = 'true'

# 테스트용 상수
TEST_API_BASE_URL = "https://api.upbit.com/v1"
SAMPLE_TICKERS = ["KRW-BTC", "KRW-ETH", "KRW-ADA", "KRW-DOT"]

@pytest.fixture(scope="session")
def test_config():
    """테스트용 전역 설정"""
    return {
        'api_base_url': TEST_API_BASE_URL,
        'rate_limit_delay': 0.1,  # 테스트에서는 짧게
        'retry_attempts': 2,
        'timeout': 5
    }

@pytest.fixture
def sample_portfolio():
    """테스트용 포트폴리오 데이터"""
    return {
        'BTC': 0.5,
        'ETH': 2.0,
        'ADA': 1000.0,
        'DOT': 50.0
    }

@pytest.fixture
def sample_ticker_data():
    """업비트 API 티커 응답 Mock 데이터"""
    return [
        {
            "market": "KRW-BTC",
            "trade_date": "20231201",
            "trade_time": "143052",
            "trade_date_kst": "20231201",
            "trade_time_kst": "233052",
            "trade_timestamp": 1701432652000,
            "opening_price": 50000000.0,
            "high_price": 52000000.0,
            "low_price": 49000000.0,
            "trade_price": 51000000.0,
            "prev_closing_price": 50500000.0,
            "change": "RISE",
            "change_price": 500000.0,
            "change_rate": 0.0099009901,
            "signed_change_price": 500000.0,
            "signed_change_rate": 0.0099009901,
            "trade_volume": 0.01,
            "acc_trade_price": 1234567890.0,
            "acc_trade_price_24h": 9876543210.0,
            "acc_trade_volume": 100.5,
            "acc_trade_volume_24h": 500.25,
            "highest_52_week_price": 60000000.0,
            "highest_52_week_date": "2023-03-15",
            "lowest_52_week_price": 20000000.0,
            "lowest_52_week_date": "2023-01-10",
            "timestamp": 1701432652000
        },
        {
            "market": "KRW-ETH",
            "trade_price": 2800000.0,
            "change": "RISE",
            "change_price": 50000.0,
            "change_rate": 0.0182,
            "signed_change_price": 50000.0,
            "signed_change_rate": 0.0182
        },
        {
            "market": "KRW-ADA",
            "trade_price": 450.0,
            "change": "FALL",
            "change_price": -10.0,
            "change_rate": -0.0217,
            "signed_change_price": -10.0,
            "signed_change_rate": -0.0217
        },
        {
            "market": "KRW-DOT",
            "trade_price": 8500.0,
            "change": "RISE",
            "change_price": 200.0,
            "change_rate": 0.0241,
            "signed_change_price": 200.0,
            "signed_change_rate": 0.0241
        }
    ]

@pytest.fixture
def sample_candle_data():
    """업비트 API 캔들 응답 Mock 데이터"""
    base_date = datetime(2023, 11, 1)
    return [
        {
            "market": "KRW-BTC",
            "candle_date_time_utc": (base_date + timedelta(days=i)).isoformat() + "Z",
            "candle_date_time_kst": (base_date + timedelta(days=i) + timedelta(hours=9)).isoformat(),
            "opening_price": 48000000 + (i * 100000),
            "high_price": 50000000 + (i * 100000),
            "low_price": 47000000 + (i * 100000),
            "trade_price": 49000000 + (i * 100000),
            "timestamp": int((base_date + timedelta(days=i)).timestamp() * 1000),
            "candle_acc_trade_price": 123456789.0,
            "candle_acc_trade_volume": 10.5,
            "prev_closing_price": 48500000 + (i * 100000)
        }
        for i in range(30)  # 30일치 데이터
    ]

@pytest.fixture
def mock_api_client():
    """API 클라이언트 Mock 객체"""
    mock = Mock()

    # 기본 응답 설정
    mock.get_ticker.return_value = [
        {"market": "KRW-BTC", "trade_price": 51000000.0},
        {"market": "KRW-ETH", "trade_price": 2800000.0}
    ]

    mock.get_candles.return_value = [
        {
            "candle_date_time_kst": "2023-12-01T09:00:00",
            "opening_price": 50000000.0,
            "high_price": 52000000.0,
            "low_price": 49000000.0,
            "trade_price": 51000000.0
        }
    ]

    mock.get_markets.return_value = [
        {"market": "KRW-BTC", "korean_name": "비트코인", "english_name": "Bitcoin"},
        {"market": "KRW-ETH", "korean_name": "이더리움", "english_name": "Ethereum"}
    ]

    return mock

@pytest.fixture
def mock_requests_session():
    """requests.Session Mock 객체"""
    with patch('requests.Session') as mock_session:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None

        mock_session.return_value.get.return_value = mock_response
        mock_session.return_value.post.return_value = mock_response

        yield mock_session

@pytest.fixture
def temp_test_file(tmp_path):
    """임시 테스트 파일 생성"""
    test_file = tmp_path / "test_data.json"
    test_data = {"test": "data", "timestamp": datetime.now().isoformat()}

    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    yield test_file

    # 정리는 pytest가 자동으로 처리

@pytest.fixture
def price_alert_scenarios():
    """가격 알림 테스트 시나리오 데이터"""
    return [
        {
            "name": "상한가 도달",
            "symbol": "BTC",
            "target_price": 52000000,
            "current_price": 51000000,
            "alert_type": "upper",
            "expected_triggered": False
        },
        {
            "name": "하한가 도달",
            "symbol": "ETH",
            "target_price": 2500000,
            "current_price": 2400000,
            "alert_type": "lower",
            "expected_triggered": True
        },
        {
            "name": "정확한 목표가 도달",
            "symbol": "ADA",
            "target_price": 450,
            "current_price": 450,
            "alert_type": "exact",
            "expected_triggered": True
        }
    ]

@pytest.fixture
def investment_scenarios():
    """투자 수익률 계산 테스트 시나리오"""
    return [
        {
            "name": "비트코인 단기 투자",
            "symbol": "BTC",
            "investment_amount": 1000000,
            "purchase_date": "2023-11-01",
            "purchase_price": 48000000,
            "current_price": 51000000,
            "expected_return_rate": 0.0625  # 6.25%
        },
        {
            "name": "이더리움 중기 투자",
            "symbol": "ETH",
            "investment_amount": 500000,
            "purchase_date": "2023-06-01",
            "purchase_price": 2400000,
            "current_price": 2800000,
            "expected_return_rate": 0.1667  # 16.67%
        },
        {
            "name": "손실 시나리오",
            "symbol": "ADA",
            "investment_amount": 100000,
            "purchase_date": "2023-10-01",
            "purchase_price": 500,
            "current_price": 450,
            "expected_return_rate": -0.1  # -10%
        }
    ]

# 테스트 실행 전/후 Hook
def pytest_configure(config):
    """테스트 설정 초기화"""
    print("\n🧪 암호화폐 분석 프로젝트 테스트 시작...")

def pytest_unconfigure(config):
    """테스트 종료 후 정리"""
    print("\n✅ 테스트 완료!")

def pytest_collection_modifyitems(config, items):
    """테스트 아이템 수정 (마커 자동 추가)"""
    for item in items:
        # 파일 경로에 따른 마커 자동 추가
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)

        # API 호출 테스트 마킹
        if "api" in item.name.lower() or "client" in item.name.lower():
            item.add_marker(pytest.mark.api)

# 테스트 결과 리포트 커스터마이징
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 실행 결과 커스터마이징"""
    outcome = yield
    rep = outcome.get_result()

    # 실패한 테스트의 추가 정보 수집
    if rep.failed:
        if hasattr(item, 'funcargs'):
            # fixture 정보 추가
            rep.extra_info = f"Fixtures used: {list(item.funcargs.keys())}"

# 느린 테스트 경고
def pytest_runtest_setup(item):
    """테스트 실행 전 설정"""
    if 'slow' in item.keywords:
        pytest.skip("slow 테스트는 --slow 옵션으로 실행하세요")