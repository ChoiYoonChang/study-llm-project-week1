"""
암호화폐 포트폴리오 분석기
사용자의 암호화폐 보유 현황을 분석하여 총 가치, 개별 가치, 비중 등을 계산
"""

import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가 (직접 실행시)
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List, Any
from utils.api_client import get_current_prices
from utils.format_utils import (
    format_currency,
    format_percentage,
    format_crypto_amount,
    create_table_header,
    create_table_row
)
from config.settings import DEFAULT_CRYPTOS


def get_current_prices_api(markets: List[str]) -> Dict[str, float]:
    """
    업비트 API를 통해 현재가를 조회하는 함수

    Args:
        markets (List[str]): 조회할 마켓 코드 리스트 ['KRW-BTC', 'KRW-ETH']

    Returns:
        Dict[str, float]: 마켓별 현재가 딕셔너리
    """
    print(f"📡 {len(markets)}개 암호화폐의 현재가를 조회 중...")

    try:
        prices = get_current_prices(markets)

        if not prices:
            print("❌ 현재가 조회에 실패했습니다.")
            return {}

        print(f"✅ {len(prices)}개 암호화폐의 현재가 조회 완료")
        return prices

    except Exception as e:
        print(f"❌ API 호출 중 오류 발생: {e}")
        return {}


def validate_portfolio(portfolio: Dict[str, float]) -> bool:
    """
    포트폴리오 데이터 유효성 검증

    Args:
        portfolio (Dict[str, float]): 포트폴리오 딕셔너리

    Returns:
        bool: 유효성 검증 결과
    """
    if not portfolio:
        print("❌ 포트폴리오가 비어있습니다.")
        return False

    for market, quantity in portfolio.items():
        if not isinstance(market, str) or not market:
            print(f"❌ 잘못된 마켓 코드: {market}")
            return False

        if not isinstance(quantity, (int, float)) or quantity < 0:
            print(f"❌ 잘못된 수량: {market} = {quantity}")
            return False

        if not market.startswith('KRW-'):
            print(f"❌ 지원하지 않는 마켓: {market} (KRW 마켓만 지원)")
            return False

    return True


def analyze_portfolio(portfolio: Dict[str, float]) -> Dict[str, Any]:
    """
    포트폴리오를 분석하여 각 암호화폐의 가치와 비중을 계산

    Args:
        portfolio (Dict[str, float]): 포트폴리오 딕셔너리
                                     예: {'KRW-BTC': 0.1, 'KRW-ETH': 2.5}

    Returns:
        Dict[str, Any]: 분석 결과
        {
            'total_value': float,           # 총 포트폴리오 가치
            'analysis': List[Dict],         # 개별 분석 결과
            'success': bool,                # 분석 성공 여부
            'error_message': str            # 오류 메시지 (실패시)
        }
    """
    print("\n🔍 포트폴리오 분석을 시작합니다...")

    # 1. 입력 데이터 검증
    if not validate_portfolio(portfolio):
        return {
            'success': False,
            'error_message': '포트폴리오 데이터가 유효하지 않습니다.',
            'total_value': 0,
            'analysis': []
        }

    # 2. 현재가 조회
    markets = list(portfolio.keys())
    current_prices = get_current_prices_api(markets)

    if not current_prices:
        return {
            'success': False,
            'error_message': '모든 암호화폐의 현재가 조회에 실패했습니다.',
            'total_value': 0,
            'analysis': []
        }
    
    # 조회되지 않은 마켓이 있는지 확인
    missing_markets = [market for market in markets if market not in current_prices]
    if missing_markets:
        print(f"⚠️  다음 마켓의 현재가를 조회할 수 없습니다: {', '.join(missing_markets)}")

    # 3. 각 암호화폐별 분석
    portfolio_analysis = []
    total_value = 0

    print("\n📊 개별 암호화폐 분석 중...")

    analyzed_markets = []
    skipped_markets = []
    
    for market, quantity in portfolio.items():
        if market not in current_prices:
            print(f"⚠️  {market}의 현재가를 찾을 수 없어 건너뜁니다.")
            skipped_markets.append(market)
            continue

        current_price = current_prices[market]
        individual_value = current_price * quantity
        total_value += individual_value
        analyzed_markets.append(market)

        # 코인명 추출 (KRW-BTC -> BTC)
        coin_name = market.split('-')[1]

        analysis_item = {
            'market': market,
            'coin_name': coin_name,
            'quantity': quantity,
            'current_price': current_price,
            'value': individual_value,
            'percentage': 0  # 비중은 나중에 계산
        }

        portfolio_analysis.append(analysis_item)
        print(f"   {coin_name}: {format_crypto_amount(quantity)} x {format_currency(current_price)} = {format_currency(individual_value)}")

    # 4. 비중 계산
    if total_value > 0:
        for item in portfolio_analysis:
            item['percentage'] = (item['value'] / total_value) * 100

    print(f"\n💰 총 포트폴리오 가치: {format_currency(total_value)}")
    
    # 스킵된 마켓이 있는 경우 요약 정보 출력
    if skipped_markets:
        print(f"⚠️  분석에서 제외된 마켓: {len(skipped_markets)}개 ({', '.join(skipped_markets)})")

    return {
        'success': True,
        'error_message': '',
        'total_value': total_value,
        'analysis': portfolio_analysis,
        'analyzed_markets': analyzed_markets,
        'skipped_markets': skipped_markets
    }


def print_portfolio_summary(analysis_result: Dict[str, Any]) -> None:
    """
    포트폴리오 분석 결과를 요약하여 출력

    Args:
        analysis_result (Dict): analyze_portfolio 함수의 결과
    """
    if not analysis_result['success']:
        print(f"\n❌ 분석 실패: {analysis_result['error_message']}")
        return

    total_value = analysis_result['total_value']
    analysis = analysis_result['analysis']

    print(f"\n" + "="*60)
    print(f"📊 포트폴리오 분석 결과 요약")
    print(f"="*60)
    print(f"💰 총 포트폴리오 가치: {format_currency(total_value)}")
    print(f"🪙 보유 암호화폐 수: {len(analysis)}개")

    if analysis:
        # 가장 비중이 높은 암호화폐 찾기
        max_holding = max(analysis, key=lambda x: x['percentage'])
        print(f"📈 최대 보유: {max_holding['coin_name']} ({format_percentage(max_holding['percentage'])})")

        # 가장 비중이 낮은 암호화폐 찾기
        min_holding = min(analysis, key=lambda x: x['percentage'])
        print(f"📉 최소 보유: {min_holding['coin_name']} ({format_percentage(min_holding['percentage'])})")


def print_portfolio_table(analysis_result: Dict[str, Any]) -> None:
    """
    포트폴리오 분석 결과를 테이블 형태로 출력

    Args:
        analysis_result (Dict): analyze_portfolio 함수의 결과
    """
    if not analysis_result['success']:
        return

    analysis = analysis_result['analysis']

    if not analysis:
        print("\n❌ 출력할 데이터가 없습니다.")
        return

    print(f"\n📋 상세 분석 결과")
    print(f"-"*80)

    # 테이블 헤더 설정
    columns = ['암호화폐', '보유수량', '현재가', '보유가치', '비중']
    widths = [10, 15, 15, 15, 10]
    alignments = ['center', 'right', 'right', 'right', 'center']

    # 헤더 출력
    print(create_table_header(columns, widths))

    # 비중순으로 정렬 (높은 순)
    sorted_analysis = sorted(analysis, key=lambda x: x['percentage'], reverse=True)

    # 각 행 출력
    for item in sorted_analysis:
        values = [
            item['coin_name'],
            format_crypto_amount(item['quantity']),
            format_currency(item['current_price']),
            format_currency(item['value']),
            format_percentage(item['percentage'])
        ]
        print(create_table_row(values, widths, alignments))

    # 총합 행 추가
    print("|" + "-"*78 + "|")
    total_row = [
        "총합",
        "-",
        "-",
        format_currency(analysis_result['total_value']),
        "100.00%"
    ]
    print(create_table_row(total_row, widths, alignments))


def get_sample_portfolio() -> Dict[str, float]:
    """
    샘플 포트폴리오를 반환 (테스트용)

    Returns:
        Dict[str, float]: 샘플 포트폴리오
    """
    return {
        "KRW-BTC": 0.05,      # 비트코인 0.05개
        "KRW-ETH": 1.2,       # 이더리움 1.2개
        "KRW-XRP": 500,       # 리플 500개
        "KRW-ADA": 1000       # 에이다 1000개
    }


def get_custom_portfolio() -> Dict[str, float]:
    """
    사용자로부터 포트폴리오 입력받기

    Returns:
        Dict[str, float]: 사용자 입력 포트폴리오
    """
    print("\n📝 포트폴리오를 입력해주세요")
    print("형식: 마켓코드 수량 (예: KRW-BTC 0.1)")
    print("입력 완료시 'done' 입력")
    print("-" * 40)

    portfolio = {}

    while True:
        try:
            user_input = input("입력 (마켓코드 수량 또는 'done'): ").strip()

            if user_input.lower() == 'done':
                break

            if not user_input:
                continue

            parts = user_input.split()
            if len(parts) != 2:
                print("❌ 형식이 잘못되었습니다. '마켓코드 수량' 형식으로 입력하세요.")
                continue

            market = parts[0].upper()
            quantity = float(parts[1])

            if not market.startswith('KRW-'):
                print("❌ KRW 마켓만 지원합니다. (예: KRW-BTC)")
                continue

            if quantity < 0:
                print("❌ 수량은 0 이상이어야 합니다.")
                continue

            portfolio[market] = quantity
            print(f"✅ 추가됨: {market} {quantity}")

        except ValueError:
            print("❌ 수량은 숫자여야 합니다.")
        except KeyboardInterrupt:
            print("\n❌ 입력이 취소되었습니다.")
            return {}

    return portfolio


def run_portfolio_analyzer():
    """
    포트폴리오 분석기 메인 실행 함수
    """
    print("\n" + "="*60)
    print("📊 암호화폐 포트폴리오 분석기")
    print("="*60)

    # 포트폴리오 선택
    print("\n포트폴리오를 선택하세요:")
    print("1. 샘플 포트폴리오 사용")
    print("2. 직접 입력")

    try:
        choice = input("선택 (1-2): ").strip()

        if choice == '1':
            portfolio = get_sample_portfolio()
            print(f"\n📋 샘플 포트폴리오 사용:")
            for market, quantity in portfolio.items():
                coin_name = market.split('-')[1]
                print(f"   {coin_name}: {format_crypto_amount(quantity)}")

        elif choice == '2':
            portfolio = get_custom_portfolio()
            if not portfolio:
                print("❌ 포트폴리오가 입력되지 않았습니다.")
                return

        else:
            print("❌ 잘못된 선택입니다.")
            return

        # 포트폴리오 분석 실행
        result = analyze_portfolio(portfolio)

        # 결과 출력
        print_portfolio_summary(result)
        print_portfolio_table(result)

        print(f"\n" + "="*60)
        print("✅ 포트폴리오 분석이 완료되었습니다!")

    except KeyboardInterrupt:
        print("\n❌ 분석이 취소되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    # 직접 실행시 테스트
    run_portfolio_analyzer()