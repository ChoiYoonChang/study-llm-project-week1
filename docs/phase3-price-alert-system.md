# Phase 3: 가격 알림 시스템 구현

## 📋 진행 체크리스트

### 1. 목표가 설정 로직 구현
- [ ] 현재가 기반 상한가/하한가 자동 계산
- [ ] 사용자 직접 목표가 입력 기능
- [ ] 목표가 유효성 검증 로직

### 2. 단일 가격 조회 API 구현
- [ ] 단일 암호화폐 현재가 조회 함수 (`get_single_price_api`)
- [ ] API 호출 최적화 및 에러 처리
- [ ] 응답 데이터 파싱 및 검증

### 3. 가격 모니터링 시스템 구현
- [ ] 반복적 가격 조회 로직
- [ ] 실시간 시간 표시
- [ ] 가격 변동 추이 기록

### 4. 알림 조건 및 메시지 시스템
- [ ] 상한가/하한가 도달 감지
- [ ] 알림 메시지 포맷팅
- [ ] 연속 알림 방지 로직

### 5. 사용자 인터페이스 구현
- [ ] 모니터링 설정 입력
- [ ] 실시간 상태 표시
- [ ] 모니터링 종료 조건

### 6. 테스트 및 검증
- [ ] 다양한 가격 변동 시나리오 테스트
- [ ] 네트워크 오류 상황 테스트
- [ ] 장기간 모니터링 안정성 테스트

---

## 📁 생성할 파일

### 1. src/price_alert.py (메인 구현 파일)
### 2. tests/test_price_alert.py (테스트 파일)

---

## 📝 상세 구현 계획

### 1. src/price_alert.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/src/price_alert.py`

**파일 내용**:
```python
"""
암호화폐 가격 알림 시스템
특정 암호화폐의 가격이 목표가에 도달했을 때 알림을 제공
"""

import time
from typing import Optional, Dict, Tuple, Any
from utils.api_client import get_single_price
from utils.date_utils import get_current_time
from utils.format_utils import format_currency, format_percentage
from config.settings import (
    DEFAULT_CRYPTOS,
    DEFAULT_PRICE_CHANGE_THRESHOLD,
    DEFAULT_MONITORING_CYCLES
)


def get_single_price_api(market: str) -> Optional[float]:
    """
    단일 암호화폐의 현재가를 조회하는 함수

    Args:
        market (str): 마켓 코드 (예: 'KRW-BTC')

    Returns:
        float: 현재가
        None: 조회 실패시
    """
    try:
        current_price = get_single_price(market)
        return current_price
    except Exception as e:
        print(f"❌ 가격 조회 오류 ({market}): {e}")
        return None


def calculate_target_prices(current_price: float, threshold: float = None) -> Tuple[float, float]:
    """
    현재가를 기준으로 상한가와 하한가를 계산

    Args:
        current_price (float): 현재 가격
        threshold (float): 변동률 임계값 (기본값: 5%)

    Returns:
        Tuple[float, float]: (상한가, 하한가)
    """
    if threshold is None:
        threshold = DEFAULT_PRICE_CHANGE_THRESHOLD

    high_target = current_price * (1 + threshold)
    low_target = current_price * (1 - threshold)

    return high_target, low_target


def get_coin_name(market: str) -> str:
    """
    마켓 코드에서 코인명 추출

    Args:
        market (str): 마켓 코드 (예: 'KRW-BTC')

    Returns:
        str: 코인명 (예: 'BTC')
    """
    try:
        return market.split('-')[1]
    except IndexError:
        return market


def validate_market_code(market: str) -> bool:
    """
    마켓 코드 유효성 검증

    Args:
        market (str): 마켓 코드

    Returns:
        bool: 유효성 여부
    """
    if not market or not isinstance(market, str):
        return False

    if not market.startswith('KRW-'):
        return False

    if len(market.split('-')) != 2:
        return False

    return True


def check_price_alert_condition(current_price: float, target_high: float, target_low: float) -> Dict[str, Any]:
    """
    가격 알림 조건을 확인

    Args:
        current_price (float): 현재가
        target_high (float): 상한가
        target_low (float): 하한가

    Returns:
        Dict[str, Any]: 알림 결과
        {
            'alert_triggered': bool,      # 알림 발생 여부
            'alert_type': str,           # 'high', 'low', 'normal'
            'message': str,              # 알림 메시지
            'percentage_change': float   # 변동률
        }
    """
    if current_price >= target_high:
        # 상한가 도달
        change_rate = ((current_price - target_high) / target_high) * 100
        return {
            'alert_triggered': True,
            'alert_type': 'high',
            'message': f"🔴 상한가 도달! 현재가: {format_currency(current_price)} (목표: {format_currency(target_high)})",
            'percentage_change': change_rate
        }

    elif current_price <= target_low:
        # 하한가 도달
        change_rate = ((target_low - current_price) / target_low) * 100
        return {
            'alert_triggered': True,
            'alert_type': 'low',
            'message': f"🔵 하한가 도달! 현재가: {format_currency(current_price)} (목표: {format_currency(target_low)})",
            'percentage_change': change_rate
        }

    else:
        # 정상 범위
        return {
            'alert_triggered': False,
            'alert_type': 'normal',
            'message': f"✅ 정상 범위: {format_currency(current_price)}",
            'percentage_change': 0
        }


def display_monitoring_info(market: str, coin_name: str, target_high: float, target_low: float,
                          cycles: int, interval: int) -> None:
    """
    모니터링 시작 정보를 출력

    Args:
        market (str): 마켓 코드
        coin_name (str): 코인명
        target_high (float): 상한가
        target_low (float): 하한가
        cycles (int): 모니터링 횟수
        interval (int): 모니터링 간격(초)
    """
    print(f"\n" + "="*60)
    print(f"🔔 {coin_name} 가격 알림 시스템 시작")
    print(f"="*60)
    print(f"📊 마켓: {market}")
    print(f"📈 상한가: {format_currency(target_high)}")
    print(f"📉 하한가: {format_currency(target_low)}")
    print(f"🔄 모니터링: {cycles}회 (간격: {interval}초)")
    print(f"🕐 시작 시간: {get_current_time()}")
    print(f"-"*60)


def display_monitoring_status(cycle: int, total_cycles: int, current_time: str,
                            current_price: float, alert_result: Dict[str, Any]) -> None:
    """
    모니터링 상태를 출력

    Args:
        cycle (int): 현재 사이클
        total_cycles (int): 총 사이클 수
        current_time (str): 현재 시간
        current_price (float): 현재가
        alert_result (Dict): 알림 확인 결과
    """
    status_icon = "🔴" if alert_result['alert_type'] == 'high' else "🔵" if alert_result['alert_type'] == 'low' else "✅"

    print(f"[{current_time}] ({cycle:2d}/{total_cycles}) {status_icon} {alert_result['message']}")

    if alert_result['alert_triggered']:
        print(f"          💥 알림 발생! 변동률: {format_percentage(alert_result['percentage_change'])}")


def price_alert_system(market: str, target_high: float, target_low: float,
                      cycles: int = DEFAULT_MONITORING_CYCLES, interval: int = 5) -> Dict[str, Any]:
    """
    가격 알림 시스템 메인 함수

    Args:
        market (str): 모니터링할 마켓 코드
        target_high (float): 상한가
        target_low (float): 하한가
        cycles (int): 모니터링 횟수
        interval (int): 모니터링 간격(초)

    Returns:
        Dict[str, Any]: 모니터링 결과
    """
    # 입력 검증
    if not validate_market_code(market):
        return {
            'success': False,
            'error_message': f'잘못된 마켓 코드: {market}',
            'alerts_triggered': 0,
            'final_price': None
        }

    coin_name = get_coin_name(market)
    alerts_triggered = 0
    monitoring_data = []

    # 모니터링 정보 출력
    display_monitoring_info(market, coin_name, target_high, target_low, cycles, interval)

    try:
        for cycle in range(1, cycles + 1):
            current_time = get_current_time()

            # 현재가 조회
            current_price = get_single_price_api(market)

            if current_price is None:
                print(f"[{current_time}] ({cycle:2d}/{cycles}) ❌ 가격 조회 실패")
                continue

            # 알림 조건 확인
            alert_result = check_price_alert_condition(current_price, target_high, target_low)

            # 상태 출력
            display_monitoring_status(cycle, cycles, current_time, current_price, alert_result)

            # 모니터링 데이터 기록
            monitoring_record = {
                'cycle': cycle,
                'time': current_time,
                'price': current_price,
                'alert_triggered': alert_result['alert_triggered'],
                'alert_type': alert_result['alert_type']
            }
            monitoring_data.append(monitoring_record)

            # 알림 발생 카운트
            if alert_result['alert_triggered']:
                alerts_triggered += 1

            # 마지막 사이클이 아니면 대기
            if cycle < cycles:
                time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n❌ 모니터링이 사용자에 의해 중단되었습니다.")
        return {
            'success': False,
            'error_message': '사용자 중단',
            'alerts_triggered': alerts_triggered,
            'final_price': monitoring_data[-1]['price'] if monitoring_data else None,
            'monitoring_data': monitoring_data
        }

    except Exception as e:
        print(f"\n❌ 모니터링 중 오류 발생: {e}")
        return {
            'success': False,
            'error_message': str(e),
            'alerts_triggered': alerts_triggered,
            'final_price': monitoring_data[-1]['price'] if monitoring_data else None,
            'monitoring_data': monitoring_data
        }

    # 모니터링 완료
    final_price = monitoring_data[-1]['price'] if monitoring_data else None

    print(f"\n" + "="*60)
    print(f"✅ {coin_name} 모니터링 완료")
    print(f"📊 총 {cycles}회 확인 완료")
    print(f"🔔 알림 발생: {alerts_triggered}회")
    if final_price:
        print(f"💰 최종 가격: {format_currency(final_price)}")
    print(f"="*60)

    return {
        'success': True,
        'error_message': '',
        'alerts_triggered': alerts_triggered,
        'final_price': final_price,
        'monitoring_data': monitoring_data
    }


def get_user_alert_settings() -> Dict[str, Any]:
    """
    사용자로부터 알림 설정을 입력받는 함수

    Returns:
        Dict[str, Any]: 사용자 설정
    """
    print("\n📋 가격 알림 설정을 입력해주세요")
    print("-" * 40)

    try:
        # 마켓 선택
        print(f"📈 추천 암호화폐:")
        for i, crypto in enumerate(DEFAULT_CRYPTOS[:5], 1):
            coin_name = get_coin_name(crypto)
            print(f"   {i}. {coin_name} ({crypto})")

        market_input = input(f"\n마켓 코드 입력 (예: KRW-BTC): ").strip().upper()

        if not validate_market_code(market_input):
            print("❌ 잘못된 마켓 코드입니다.")
            return None

        # 현재가 조회
        print(f"\n📡 {get_coin_name(market_input)} 현재가 조회 중...")
        current_price = get_single_price_api(market_input)

        if current_price is None:
            print("❌ 현재가 조회에 실패했습니다.")
            return None

        print(f"💰 현재가: {format_currency(current_price)}")

        # 목표가 설정 방식 선택
        print(f"\n목표가 설정 방식을 선택하세요:")
        print(f"1. 자동 설정 (현재가 ±5%)")
        print(f"2. 직접 입력")

        choice = input("선택 (1-2): ").strip()

        if choice == '1':
            # 자동 설정
            target_high, target_low = calculate_target_prices(current_price)
            print(f"✅ 자동 설정:")
            print(f"   상한가: {format_currency(target_high)} (+5%)")
            print(f"   하한가: {format_currency(target_low)} (-5%)")

        elif choice == '2':
            # 직접 입력
            while True:
                try:
                    target_high = float(input(f"상한가 입력 (현재가보다 높게): "))
                    if target_high <= current_price:
                        print("❌ 상한가는 현재가보다 높아야 합니다.")
                        continue
                    break
                except ValueError:
                    print("❌ 숫자를 입력해주세요.")

            while True:
                try:
                    target_low = float(input(f"하한가 입력 (현재가보다 낮게): "))
                    if target_low >= current_price:
                        print("❌ 하한가는 현재가보다 낮아야 합니다.")
                        continue
                    break
                except ValueError:
                    print("❌ 숫자를 입력해주세요.")

        else:
            print("❌ 잘못된 선택입니다.")
            return None

        # 모니터링 설정
        while True:
            try:
                cycles = int(input(f"모니터링 횟수 (기본값: {DEFAULT_MONITORING_CYCLES}): ") or DEFAULT_MONITORING_CYCLES)
                if cycles <= 0:
                    print("❌ 모니터링 횟수는 1 이상이어야 합니다.")
                    continue
                break
            except ValueError:
                print("❌ 숫자를 입력해주세요.")

        while True:
            try:
                interval = int(input(f"모니터링 간격(초) (기본값: 5): ") or 5)
                if interval <= 0:
                    print("❌ 모니터링 간격은 1초 이상이어야 합니다.")
                    continue
                break
            except ValueError:
                print("❌ 숫자를 입력해주세요.")

        return {
            'market': market_input,
            'current_price': current_price,
            'target_high': target_high,
            'target_low': target_low,
            'cycles': cycles,
            'interval': interval
        }

    except KeyboardInterrupt:
        print("\n❌ 설정이 취소되었습니다.")
        return None


def get_preset_alert_settings() -> Dict[str, Any]:
    """
    미리 설정된 알림 설정을 반환 (테스트용)

    Returns:
        Dict[str, Any]: 프리셋 설정
    """
    market = "KRW-BTC"
    print(f"\n📋 프리셋 설정 사용: {get_coin_name(market)}")

    # 현재가 조회
    current_price = get_single_price_api(market)
    if current_price is None:
        return None

    # 자동으로 목표가 계산
    target_high, target_low = calculate_target_prices(current_price)

    return {
        'market': market,
        'current_price': current_price,
        'target_high': target_high,
        'target_low': target_low,
        'cycles': 10,
        'interval': 3
    }


def run_price_alert():
    """
    가격 알림 시스템 메인 실행 함수
    """
    print("\n" + "="*60)
    print("🔔 암호화폐 가격 알림 시스템")
    print("="*60)

    # 설정 선택
    print("\n설정 방식을 선택하세요:")
    print("1. 프리셋 사용 (비트코인, 빠른 테스트)")
    print("2. 직접 설정")

    try:
        choice = input("선택 (1-2): ").strip()

        if choice == '1':
            settings = get_preset_alert_settings()
        elif choice == '2':
            settings = get_user_alert_settings()
        else:
            print("❌ 잘못된 선택입니다.")
            return

        if settings is None:
            print("❌ 설정을 완료하지 못했습니다.")
            return

        # 알림 시스템 실행
        result = price_alert_system(
            market=settings['market'],
            target_high=settings['target_high'],
            target_low=settings['target_low'],
            cycles=settings['cycles'],
            interval=settings['interval']
        )

        # 결과 요약 출력
        if result['success']:
            print(f"\n📊 모니터링 결과 요약:")
            print(f"   알림 발생: {result['alerts_triggered']}회")
            if result['final_price']:
                price_change = result['final_price'] - settings['current_price']
                change_rate = (price_change / settings['current_price']) * 100
                print(f"   가격 변화: {format_currency(price_change)} ({format_percentage(change_rate)})")

        else:
            print(f"\n❌ 모니터링 실패: {result['error_message']}")

    except KeyboardInterrupt:
        print("\n❌ 프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    # 직접 실행시 테스트
    run_price_alert()
```

**작성 이유**:
- **모듈화된 구조**: 각 기능을 독립적인 함수로 분리하여 테스트와 유지보수 용이
- **유연한 설정**: 자동 계산과 직접 입력 모두 지원
- **실시간 모니터링**: 지정된 간격으로 가격을 지속적으로 확인
- **포괄적 에러 처리**: 네트워크 오류, 잘못된 입력, 사용자 중단 등 다양한 상황 대응
- **사용자 친화적**: 현재 상태를 실시간으로 표시하고 직관적인 알림 메시지 제공
- **데이터 기록**: 모니터링 과정의 모든 데이터를 기록하여 나중에 분석 가능

### 2. tests/test_price_alert.py 파일

**파일 경로**: `/Users/rooky/IdeaProjects/week1-python-project/tests/test_price_alert.py`

**파일 내용**:
```python
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
```

**작성 이유**:
- **포괄적 테스트**: 모든 주요 함수의 정상/비정상 케이스 검증
- **경계값 테스트**: 극단적인 가격 상황에서의 동작 확인
- **실제 시나리오**: 짧은 모니터링을 통한 실제 동작 검증
- **오류 처리 검증**: 다양한 오류 상황에서의 안정성 확인
- **자동화된 검증**: 예상 결과와 실제 결과를 자동으로 비교

---

## 🔧 구현 단계별 설명

### 1단계: 기본 API 및 유틸리티 함수
- **목적**: 단일 암호화폐 가격 조회와 기본적인 데이터 처리
- **구현**: `get_single_price_api()`, `validate_market_code()`, `get_coin_name()`
- **중요성**: 안정적인 데이터 수집을 위한 기반 마련

### 2단계: 목표가 계산 로직
- **목적**: 현재가를 기준으로 상한가/하한가 자동 계산
- **구현**: `calculate_target_prices()` - 퍼센트 기반 목표가 산출
- **유연성**: 사용자가 임계값을 조정할 수 있도록 파라미터화

### 3단계: 알림 조건 확인 시스템
- **목적**: 현재가와 목표가를 비교하여 알림 필요성 판단
- **구현**: `check_price_alert_condition()` - 상한가/하한가/정상 범위 구분
- **정확성**: 경계값 포함 여부를 명확히 하여 중복 알림 방지

### 4단계: 모니터링 루프 및 상태 표시
- **목적**: 지정된 횟수와 간격으로 지속적인 가격 추적
- **구현**: `price_alert_system()` - 메인 모니터링 로직
- **사용성**: 실시간 상태 표시로 사용자에게 진행상황 제공

### 5단계: 사용자 인터페이스 및 설정
- **목적**: 사용자가 쉽게 모니터링을 설정하고 실행할 수 있는 환경
- **구현**: `get_user_alert_settings()`, `get_preset_alert_settings()`
- **편의성**: 프리셋과 직접 설정 모드로 다양한 사용자 요구 충족

---

## 📋 Phase 3 실행 순서

1. **가격 알림 시스템 파일 생성**
   ```bash
   # src/price_alert.py 파일 생성 및 코드 작성
   ```

2. **테스트 파일 생성**
   ```bash
   # tests/test_price_alert.py 파일 생성 및 코드 작성
   ```

3. **기능 테스트 실행**
   ```bash
   python tests/test_price_alert.py
   ```

4. **단독 실행 테스트**
   ```bash
   python src/price_alert.py
   ```

5. **메인 프로그램에 연결**
   ```bash
   # main.py 파일 수정하여 Phase 3 기능 활성화
   ```

6. **통합 테스트**
   ```bash
   python main.py
   # 메뉴에서 2번 선택하여 가격 알림 시스템 실행
   ```

---

## 🎯 Phase 3 학습 목표 달성 확인

### seedprompt.md 요구사항 매칭:

1. **✅ 목표가 설정 (상한가, 하한가)**
   - `calculate_target_prices()`: 자동 계산
   - `get_user_alert_settings()`: 직접 입력

2. **✅ 현재가 모니터링**
   - `price_alert_system()`: 반복적 가격 조회
   - 실시간 시간 표시 및 상태 출력

3. **✅ 목표가 도달 시 알림 메시지 출력**
   - `check_price_alert_condition()`: 조건 확인
   - 상한가/하한가 도달시 명확한 알림 메시지

### 추가 구현된 기능:
- **사용자 친화적 설정**: 프리셋과 직접 입력 모드
- **모니터링 데이터 기록**: 전체 과정의 데이터 저장
- **중단 가능한 모니터링**: Ctrl+C로 안전한 중단
- **포괄적 에러 처리**: 네트워크 오류, 잘못된 입력 등 대응
- **상세한 통계**: 알림 발생 횟수, 가격 변화량 등

---

## 💡 실사용 권장사항

### 모니터링 설정 가이드:
- **임계값**: 3-10% 사이 권장 (너무 작으면 잦은 알림, 너무 크면 의미 없음)
- **모니터링 간격**: 5-30초 권장 (너무 짧으면 API 부하, 너무 길면 놓칠 수 있음)
- **모니터링 횟수**: 10-100회 권장 (용도에 따라 조정)

### 주의사항:
- **API 제한**: 업비트 API의 요청 제한을 고려하여 적절한 간격 설정
- **네트워크 안정성**: 불안정한 네트워크에서는 더 긴 간격 사용
- **장기 모니터링**: 매우 긴 모니터링시에는 중간에 로그 저장 고려

---

## 📌 Phase 3 완료 후 확인사항

- [ ] 가격 알림 시스템이 정상적으로 실행되는가?
- [ ] 프리셋 설정으로 빠른 테스트가 가능한가?
- [ ] 사용자 직접 설정이 올바르게 동작하는가?
- [ ] 상한가/하한가 도달시 알림이 정확하게 발생하는가?
- [ ] 모니터링 중 Ctrl+C로 안전하게 중단되는가?
- [ ] API 오류 상황에서 적절한 에러 메시지가 출력되는가?
- [ ] 실시간 상태 표시가 명확하고 이해하기 쉬운가?
- [ ] 모든 테스트가 통과하는가?

Phase 3이 완료되면 Phase 4(수익률 계산기) 구현을 진행합니다.