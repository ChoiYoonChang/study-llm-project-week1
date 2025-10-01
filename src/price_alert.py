"""
암호화폐 가격 알림 시스템
특정 암호화폐의 가격이 목표가에 도달했을 때 알림을 제공
"""

import sys
import os
import time

# 프로젝트 루트 디렉토리를 Python 경로에 추가 (직접 실행시)
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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