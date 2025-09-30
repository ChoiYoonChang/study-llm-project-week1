"""
프로젝트 전역 설정 파일
업비트 API 관련 설정 및 상수 정의
"""

# 업비트 API 기본 설정
UPBIT_API_BASE_URL = "https://api.upbit.com/v1"

# API 엔드포인트
API_ENDPOINTS = {
    "ticker": f"{UPBIT_API_BASE_URL}/ticker",
    "candles_days": f"{UPBIT_API_BASE_URL}/candles/days",
    "market_all": f"{UPBIT_API_BASE_URL}/market/all"
}

# 요청 설정
REQUEST_TIMEOUT = 10  # 초
MAX_RETRIES = 3

# 출력 포맷 설정
CURRENCY_FORMAT = "{:,.0f}"
PERCENTAGE_FORMAT = "{:.2f}"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"

# 기본 암호화폐 목록 (테스트용)
DEFAULT_CRYPTOS = [
    "KRW-BTC",  # 비트코인
    "KRW-ETH",  # 이더리움
    "KRW-XRP",  # 리플
    "KRW-ADA",  # 에이다
    "KRW-DOT"   # 폴카닷
]

# 알림 시스템 기본 설정
DEFAULT_PRICE_CHANGE_THRESHOLD = 0.05  # 5% 변동률
DEFAULT_MONITORING_CYCLES = 10  # 기본 모니터링 횟수
MONITORING_INTERVAL = 5  # 초 (실제 구현시 사용)