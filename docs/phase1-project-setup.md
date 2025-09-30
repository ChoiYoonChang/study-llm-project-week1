# Phase 1: 프로젝트 초기 설정 및 구조 설계

## 📋 진행 체크리스트

### 1. 프로젝트 디렉토리 구조 설정
- [ ] 메인 프로젝트 디렉토리 확인
- [ ] `src/` 디렉토리 생성 (소스코드 파일들)
- [ ] `utils/` 디렉토리 생성 (공통 유틸리티 함수들)
- [ ] `config/` 디렉토리 생성 (설정 파일들)
- [ ] `tests/` 디렉토리 생성 (테스트 파일들)

### 2. 필수 라이브러리 설치 및 설정
- [ ] `requirements.txt` 파일 생성
- [ ] 필수 라이브러리 설치 (`pip install -r requirements.txt`)
- [ ] `.gitignore` 파일 생성

### 3. 기본 설정 파일 작성
- [ ] API 설정 파일 작성
- [ ] 공통 상수 정의 파일 작성

### 4. 공통 유틸리티 함수 작성
- [ ] API 호출 기본 함수 작성
- [ ] 날짜/시간 처리 함수 작성
- [ ] 포맷팅 유틸리티 함수 작성

---

## 📁 생성할 파일 및 디렉토리 구조

```
week1-python-project/
├── src/
│   ├── __init__.py
│   ├── portfolio_analyzer.py     # Phase 2에서 작성
│   ├── price_alert.py           # Phase 3에서 작성
│   └── return_calculator.py     # Phase 4에서 작성
├── utils/
│   ├── __init__.py
│   ├── api_client.py
│   ├── date_utils.py
│   └── format_utils.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── tests/
│   ├── __init__.py
│   └── test_api_client.py
├── requirements.txt
├── .gitignore
└── main.py
```

---

## 📝 상세 구현 계획

### 1. requirements.txt 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/requirements.txt`

**파일 내용**:
```
requests==2.31.0
datetime
```

**작성 이유**:
- `requests`: 업비트 API 호출을 위한 HTTP 라이브러리
- `datetime`: 시간 관련 처리를 위한 표준 라이브러리 (Python 내장이지만 명시적 표기)

### 2. .gitignore 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/.gitignore`

**파일 내용**:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyCharm
.idea/

# VS Code
.vscode/

# Environment variables
.env

# Test coverage
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover
.hypothesis/
.pytest_cache/
```

**작성 이유**:
- Python 컴파일 파일, IDE 설정 파일, 임시 파일들을 git 추적에서 제외
- 보안상 중요한 환경변수 파일 제외

### 3. config/settings.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/config/settings.py`

**파일 내용**:
```python
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
```

**작성 이유**:
- 프로젝트 전반에서 사용할 상수들을 중앙집중식으로 관리
- API URL과 설정값들을 하드코딩하지 않고 설정 파일로 분리
- 나중에 설정 변경시 이 파일만 수정하면 되도록 구조화

### 4. config/__init__.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/config/__init__.py`

**파일 내용**:
```python
"""
설정 모듈 초기화 파일
"""

from .settings import (
    UPBIT_API_BASE_URL,
    API_ENDPOINTS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    CURRENCY_FORMAT,
    PERCENTAGE_FORMAT,
    DATETIME_FORMAT,
    TIME_FORMAT,
    DEFAULT_CRYPTOS,
    DEFAULT_PRICE_CHANGE_THRESHOLD,
    DEFAULT_MONITORING_CYCLES,
    MONITORING_INTERVAL
)

__all__ = [
    'UPBIT_API_BASE_URL',
    'API_ENDPOINTS',
    'REQUEST_TIMEOUT',
    'MAX_RETRIES',
    'CURRENCY_FORMAT',
    'PERCENTAGE_FORMAT',
    'DATETIME_FORMAT',
    'TIME_FORMAT',
    'DEFAULT_CRYPTOS',
    'DEFAULT_PRICE_CHANGE_THRESHOLD',
    'DEFAULT_MONITORING_CYCLES',
    'MONITORING_INTERVAL'
]
```

**작성 이유**:
- config 모듈을 패키지로 만들어 다른 모듈에서 쉽게 import 가능
- 설정값들을 명시적으로 export하여 코드 가독성 향상

### 5. utils/api_client.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/utils/api_client.py`

**파일 내용**:
```python
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
```

**작성 이유**:
- API 호출 로직을 중앙집중화하여 코드 중복 방지
- 에러 처리와 재시도 로직을 공통으로 적용
- 타입 힌트를 사용하여 코드 안정성 향상
- 각 Phase에서 필요한 API 호출 패턴을 미리 구현

### 6. utils/date_utils.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/utils/date_utils.py`

**파일 내용**:
```python
"""
날짜 및 시간 처리 유틸리티 함수들
"""

from datetime import datetime, timedelta
from config.settings import DATETIME_FORMAT, TIME_FORMAT


def get_current_time() -> str:
    """
    현재 시간을 HH:MM:SS 형식으로 반환

    Returns:
        str: 현재 시간 문자열
    """
    return datetime.now().strftime(TIME_FORMAT)


def get_current_datetime() -> str:
    """
    현재 날짜와 시간을 YYYY-MM-DD HH:MM:SS 형식으로 반환

    Returns:
        str: 현재 날짜시간 문자열
    """
    return datetime.now().strftime(DATETIME_FORMAT)


def get_date_days_ago(days: int) -> datetime:
    """
    지정한 일수만큼 이전 날짜를 반환

    Args:
        days (int): 며칠 전인지

    Returns:
        datetime: 계산된 날짜
    """
    return datetime.now() - timedelta(days=days)


def format_date(date_obj: datetime, format_str: str = DATETIME_FORMAT) -> str:
    """
    datetime 객체를 지정된 형식의 문자열로 변환

    Args:
        date_obj (datetime): 변환할 datetime 객체
        format_str (str): 날짜 형식 문자열

    Returns:
        str: 형식화된 날짜 문자열
    """
    return date_obj.strftime(format_str)


def parse_upbit_datetime(upbit_date_str: str) -> datetime:
    """
    업비트 API에서 받은 날짜 문자열을 datetime 객체로 변환
    업비트 API는 ISO 8601 형식을 사용 (예: "2024-01-01T00:00:00")

    Args:
        upbit_date_str (str): 업비트 API 날짜 문자열

    Returns:
        datetime: 변환된 datetime 객체
    """
    try:
        # 'T'로 날짜와 시간이 구분되고, 'Z'나 '+09:00' 같은 타임존 정보 제거
        date_part = upbit_date_str.split('T')[0]
        time_part = upbit_date_str.split('T')[1].split('+')[0].split('Z')[0]

        datetime_str = f"{date_part} {time_part}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, IndexError) as e:
        print(f"날짜 파싱 오류: {upbit_date_str}, 에러: {e}")
        return datetime.now()
```

**작성 이유**:
- 날짜/시간 처리 로직을 공통화하여 일관된 형식 보장
- 업비트 API 응답의 날짜 형식을 파싱하는 함수 제공
- Phase 2, 3, 4에서 공통으로 사용할 시간 관련 기능들을 미리 구현

### 7. utils/format_utils.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/utils/format_utils.py`

**파일 내용**:
```python
"""
데이터 포맷팅 유틸리티 함수들
숫자, 통화, 퍼센트 등의 형식화를 담당
"""

from config.settings import CURRENCY_FORMAT, PERCENTAGE_FORMAT


def format_currency(amount: float, currency: str = "원") -> str:
    """
    숫자를 통화 형식으로 포맷팅

    Args:
        amount (float): 금액
        currency (str): 통화 단위

    Returns:
        str: 포맷팅된 통화 문자열
    """
    formatted_amount = CURRENCY_FORMAT.format(amount)
    return f"{formatted_amount}{currency}"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    숫자를 퍼센트 형식으로 포맷팅

    Args:
        value (float): 퍼센트 값 (이미 %로 계산된 값)
        decimal_places (int): 소수점 자리수

    Returns:
        str: 포맷팅된 퍼센트 문자열
    """
    format_str = f"{{:.{decimal_places}f}}"
    return f"{format_str.format(value)}%"


def format_crypto_amount(amount: float, decimal_places: int = 8) -> str:
    """
    암호화폐 수량을 적절한 형식으로 포맷팅

    Args:
        amount (float): 암호화폐 수량
        decimal_places (int): 소수점 자리수

    Returns:
        str: 포맷팅된 수량 문자열
    """
    # 매우 작은 수는 지수표기법 사용
    if amount < 0.0001:
        return f"{amount:.2e}"
    else:
        format_str = f"{{:.{decimal_places}f}}"
        return format_str.format(amount).rstrip('0').rstrip('.')


def format_price_change(current_price: float, previous_price: float) -> tuple:
    """
    가격 변동을 계산하고 포맷팅

    Args:
        current_price (float): 현재가
        previous_price (float): 이전가

    Returns:
        tuple: (변동액, 변동률, 상승/하락 표시)
    """
    if previous_price == 0:
        return "0원", "0.00%", "→"

    change_amount = current_price - previous_price
    change_rate = (change_amount / previous_price) * 100

    # 상승/하락/보합 표시
    if change_amount > 0:
        direction = "▲"
        sign = "+"
    elif change_amount < 0:
        direction = "▼"
        sign = ""  # 음수 기호는 자동으로 포함됨
    else:
        direction = "→"
        sign = ""

    formatted_amount = format_currency(abs(change_amount))
    formatted_rate = format_percentage(abs(change_rate))

    return f"{sign}{formatted_amount}", f"{sign}{formatted_rate}", direction


def create_table_header(columns: list, widths: list) -> str:
    """
    테이블 헤더를 생성

    Args:
        columns (list): 컬럼명 리스트
        widths (list): 각 컬럼의 너비

    Returns:
        str: 포맷팅된 테이블 헤더
    """
    header_parts = []
    for col, width in zip(columns, widths):
        header_parts.append(f"{col:^{width}}")

    header = "| " + " | ".join(header_parts) + " |"
    separator = "|" + "|".join(["-" * (width + 2) for width in widths]) + "|"

    return f"{header}\n{separator}"


def create_table_row(values: list, widths: list, alignments: list = None) -> str:
    """
    테이블 행을 생성

    Args:
        values (list): 값들의 리스트
        widths (list): 각 컬럼의 너비
        alignments (list): 정렬 방식 ('left', 'center', 'right')

    Returns:
        str: 포맷팅된 테이블 행
    """
    if alignments is None:
        alignments = ['left'] * len(values)

    row_parts = []
    for value, width, alignment in zip(values, widths, alignments):
        if alignment == 'center':
            formatted_value = f"{str(value):^{width}}"
        elif alignment == 'right':
            formatted_value = f"{str(value):>{width}}"
        else:  # left
            formatted_value = f"{str(value):<{width}}"
        row_parts.append(formatted_value)

    return "| " + " | ".join(row_parts) + " |"
```

**작성 이유**:
- 일관된 출력 형식을 보장하기 위한 공통 포맷팅 함수들
- 테이블 형식의 결과 출력을 위한 유틸리티 함수
- 암호화폐 특성에 맞는 소수점 처리 및 가격 변동 표시
- Phase 2, 3, 4의 결과 출력에서 공통으로 사용

### 8. utils/__init__.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/utils/__init__.py`

**파일 내용**:
```python
"""
유틸리티 모듈 초기화 파일
"""

from .api_client import (
    make_api_request,
    get_current_prices,
    get_single_price,
    get_historical_data
)

from .date_utils import (
    get_current_time,
    get_current_datetime,
    get_date_days_ago,
    format_date,
    parse_upbit_datetime
)

from .format_utils import (
    format_currency,
    format_percentage,
    format_crypto_amount,
    format_price_change,
    create_table_header,
    create_table_row
)

__all__ = [
    # API 관련
    'make_api_request',
    'get_current_prices',
    'get_single_price',
    'get_historical_data',

    # 날짜 관련
    'get_current_time',
    'get_current_datetime',
    'get_date_days_ago',
    'format_date',
    'parse_upbit_datetime',

    # 포맷팅 관련
    'format_currency',
    'format_percentage',
    'format_crypto_amount',
    'format_price_change',
    'create_table_header',
    'create_table_row'
]
```

**작성 이유**:
- utils 패키지의 모든 함수들을 쉽게 import할 수 있도록 설정
- 모듈별로 기능을 분류하여 코드 구조의 명확성 제공

### 9. src/__init__.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/src/__init__.py`

**파일 내용**:
```python
"""
메인 소스코드 모듈 초기화 파일
"""

# 각 Phase별 구현이 완료되면 여기에 import 추가 예정
# from .portfolio_analyzer import analyze_portfolio
# from .price_alert import price_alert_system
# from .return_calculator import calculate_investment_return

__all__ = []
```

**작성 이유**:
- 향후 각 Phase에서 구현할 메인 기능들을 패키지로 관리
- 현재는 빈 상태로 두고 각 Phase 구현시 점진적으로 추가

### 10. main.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/main.py`

**파일 내용**:
```python
"""
암호화폐 분석 프로젝트 메인 실행 파일
사용자 인터페이스 및 메뉴 시스템 제공
"""

def print_welcome_message():
    """프로젝트 시작 환영 메시지"""
    print("=" * 60)
    print("🚀 암호화폐 분석 프로젝트에 오신 것을 환영합니다!")
    print("=" * 60)
    print("이 프로젝트는 업비트 API를 활용한 암호화폐 분석 도구입니다.")
    print()


def show_menu():
    """메인 메뉴 출력"""
    print("\n📋 메뉴를 선택하세요:")
    print("1. 포트폴리오 분석기 (Phase 2)")
    print("2. 가격 알림 시스템 (Phase 3)")
    print("3. 수익률 계산기 (Phase 4)")
    print("4. 종료")
    print("-" * 40)


def main():
    """메인 실행 함수"""
    print_welcome_message()

    while True:
        show_menu()
        try:
            choice = input("선택 (1-4): ").strip()

            if choice == '1':
                print("\n📊 포트폴리오 분석기")
                print("🚧 Phase 2에서 구현 예정입니다.")
                # TODO: Phase 2 구현 후 import 및 함수 호출 추가
                # from src.portfolio_analyzer import run_portfolio_analyzer
                # run_portfolio_analyzer()

            elif choice == '2':
                print("\n🔔 가격 알림 시스템")
                print("🚧 Phase 3에서 구현 예정입니다.")
                # TODO: Phase 3 구현 후 import 및 함수 호출 추가
                # from src.price_alert import run_price_alert
                # run_price_alert()

            elif choice == '3':
                print("\n📈 수익률 계산기")
                print("🚧 Phase 4에서 구현 예정입니다.")
                # TODO: Phase 4 구현 후 import 및 함수 호출 추가
                # from src.return_calculator import run_return_calculator
                # run_return_calculator()

            elif choice == '4':
                print("\n👋 프로그램을 종료합니다. 감사합니다!")
                break

            else:
                print("❌ 잘못된 선택입니다. 1-4 사이의 숫자를 입력하세요.")

        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
```

**작성 이유**:
- 사용자가 프로젝트의 각 기능을 쉽게 접근할 수 있는 통합 인터페이스 제공
- Phase별 구현 상태를 명확히 표시하여 개발 진행사항 추적 가능
- 향후 각 Phase 완료시 해당 기능을 쉽게 연결할 수 있는 구조

### 11. tests/__init__.py 및 기본 테스트 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/tests/__init__.py`

**파일 내용**:
```python
"""
테스트 모듈 초기화 파일
"""
```

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/tests/test_api_client.py`

**파일 내용**:
```python
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
```

**작성 이유**:
- Phase 1에서 구현한 기본 기능들이 정상 작동하는지 확인
- API 연결 상태 및 데이터 받아오기 기능 검증
- 포맷팅 함수들의 출력 결과 확인

---

## 🚀 Phase 1 실행 순서

1. **디렉토리 구조 생성**
   ```bash
   mkdir -p src utils config tests
   ```

2. **필수 파일들 생성** (위에서 제시한 모든 파일들을 순서대로 생성)

3. **라이브러리 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **기본 테스트 실행**
   ```bash
   python tests/test_api_client.py
   ```

5. **메인 프로그램 실행**
   ```bash
   python main.py
   ```

---

## 📌 Phase 1 완료 후 확인사항

- [ ] 모든 디렉토리와 파일이 정상적으로 생성되었는가?
- [ ] API 연결 테스트가 성공했는가?
- [ ] 메인 프로그램이 정상적으로 실행되는가?
- [ ] 각 유틸리티 함수들이 예상대로 동작하는가?

Phase 1이 완료되면 Phase 2(포트폴리오 분석기) 구현을 위한 기반이 준비됩니다.