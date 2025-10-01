"""
테스트 데이터 생성 헬퍼
다양한 테스트 시나리오를 위한 Mock 데이터 생성기
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from faker import Faker

fake = Faker('ko_KR')

class TestDataGenerator:
    """테스트용 데이터 생성 클래스"""

    @staticmethod
    def generate_ticker_data(
        market: str = "KRW-BTC",
        base_price: float = 50000000.0,
        volatility: float = 0.05
    ) -> Dict[str, Any]:
        """
        업비트 티커 데이터 생성

        Args:
            market: 마켓 코드 (예: KRW-BTC)
            base_price: 기준 가격
            volatility: 변동성 (0.0~1.0)
        """
        change_rate = random.uniform(-volatility, volatility)
        change_price = base_price * change_rate
        trade_price = base_price + change_price

        return {
            "market": market,
            "trade_date": datetime.now().strftime("%Y%m%d"),
            "trade_time": datetime.now().strftime("%H%M%S"),
            "trade_date_kst": datetime.now().strftime("%Y%m%d"),
            "trade_time_kst": datetime.now().strftime("%H%M%S"),
            "trade_timestamp": int(datetime.now().timestamp() * 1000),
            "opening_price": base_price * random.uniform(0.98, 1.02),
            "high_price": max(base_price, trade_price) * random.uniform(1.0, 1.03),
            "low_price": min(base_price, trade_price) * random.uniform(0.97, 1.0),
            "trade_price": trade_price,
            "prev_closing_price": base_price,
            "change": "RISE" if change_price > 0 else "FALL" if change_price < 0 else "EVEN",
            "change_price": abs(change_price),
            "change_rate": abs(change_rate),
            "signed_change_price": change_price,
            "signed_change_rate": change_rate,
            "trade_volume": random.uniform(0.01, 10.0),
            "acc_trade_price": random.uniform(1000000000, 10000000000),
            "acc_trade_price_24h": random.uniform(5000000000, 50000000000),
            "acc_trade_volume": random.uniform(100, 1000),
            "acc_trade_volume_24h": random.uniform(500, 5000),
            "highest_52_week_price": trade_price * random.uniform(1.2, 2.0),
            "highest_52_week_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "lowest_52_week_price": trade_price * random.uniform(0.3, 0.8),
            "lowest_52_week_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "timestamp": int(datetime.now().timestamp() * 1000)
        }

    @staticmethod
    def generate_candle_data(
        market: str = "KRW-BTC",
        count: int = 30,
        base_price: float = 50000000.0,
        trend: str = "random"  # "up", "down", "random", "sideways"
    ) -> List[Dict[str, Any]]:
        """
        업비트 캔들 데이터 생성

        Args:
            market: 마켓 코드
            count: 생성할 캔들 개수
            base_price: 시작 가격
            trend: 트렌드 방향
        """
        candles = []
        current_price = base_price

        for i in range(count):
            date = datetime.now() - timedelta(days=count - i - 1)

            # 트렌드에 따른 가격 변화
            if trend == "up":
                price_change = random.uniform(0.005, 0.03)
            elif trend == "down":
                price_change = random.uniform(-0.03, -0.005)
            elif trend == "sideways":
                price_change = random.uniform(-0.01, 0.01)
            else:  # random
                price_change = random.uniform(-0.05, 0.05)

            current_price *= (1 + price_change)

            # OHLC 데이터 생성
            high_price = current_price * random.uniform(1.0, 1.02)
            low_price = current_price * random.uniform(0.98, 1.0)
            opening_price = current_price * random.uniform(0.995, 1.005)

            candle = {
                "market": market,
                "candle_date_time_utc": date.isoformat() + "Z",
                "candle_date_time_kst": (date + timedelta(hours=9)).isoformat(),
                "opening_price": opening_price,
                "high_price": high_price,
                "low_price": low_price,
                "trade_price": current_price,
                "timestamp": int(date.timestamp() * 1000),
                "candle_acc_trade_price": random.uniform(100000000, 1000000000),
                "candle_acc_trade_volume": random.uniform(10, 100),
                "prev_closing_price": current_price * random.uniform(0.99, 1.01)
            }
            candles.append(candle)

        return candles

    @staticmethod
    def generate_portfolio(
        symbols: Optional[List[str]] = None,
        total_value_range: tuple = (1000000, 10000000)
    ) -> Dict[str, float]:
        """
        랜덤 포트폴리오 생성

        Args:
            symbols: 포함할 암호화폐 심볼 리스트
            total_value_range: 총 투자금액 범위
        """
        if symbols is None:
            symbols = ["BTC", "ETH", "ADA", "DOT", "XRP", "DOGE"]

        # 랜덤하게 3-5개 선택
        selected_symbols = random.sample(symbols, random.randint(3, min(5, len(symbols))))

        portfolio = {}
        prices = {
            "BTC": 50000000,
            "ETH": 2800000,
            "ADA": 450,
            "DOT": 8500,
            "XRP": 650,
            "DOGE": 150
        }

        total_value = random.uniform(*total_value_range)
        remaining_value = total_value

        for i, symbol in enumerate(selected_symbols):
            if i == len(selected_symbols) - 1:  # 마지막 심볼
                value = remaining_value
            else:
                value = remaining_value * random.uniform(0.1, 0.5)
                remaining_value -= value

            quantity = value / prices.get(symbol, 1000000)
            portfolio[symbol] = round(quantity, 8)

        return portfolio

    @staticmethod
    def generate_price_alerts(count: int = 5) -> List[Dict[str, Any]]:
        """
        가격 알림 테스트 데이터 생성

        Args:
            count: 생성할 알림 개수
        """
        symbols = ["BTC", "ETH", "ADA", "DOT", "XRP"]
        prices = {
            "BTC": 50000000,
            "ETH": 2800000,
            "ADA": 450,
            "DOT": 8500,
            "XRP": 650
        }

        alerts = []
        for _ in range(count):
            symbol = random.choice(symbols)
            current_price = prices[symbol]
            alert_type = random.choice(["upper", "lower"])

            if alert_type == "upper":
                target_price = current_price * random.uniform(1.05, 1.3)
            else:
                target_price = current_price * random.uniform(0.7, 0.95)

            alert = {
                "symbol": symbol,
                "target_price": target_price,
                "current_price": current_price,
                "alert_type": alert_type,
                "created_at": fake.date_time_between(start_date="-7d", end_date="now"),
                "is_active": random.choice([True, True, True, False])  # 75% 활성
            }
            alerts.append(alert)

        return alerts

    @staticmethod
    def generate_investment_scenario(
        symbol: str = "BTC",
        investment_amount: float = 1000000,
        days_ago: int = 30
    ) -> Dict[str, Any]:
        """
        투자 시나리오 생성

        Args:
            symbol: 투자 암호화폐
            investment_amount: 투자 금액
            days_ago: 투자한 날로부터 현재까지 일수
        """
        prices = {
            "BTC": 50000000,
            "ETH": 2800000,
            "ADA": 450,
            "DOT": 8500,
            "XRP": 650
        }

        current_price = prices.get(symbol, 1000000)

        # 과거 가격 (랜덤 변화)
        price_change = random.uniform(-0.5, 1.0)  # -50% ~ +100%
        past_price = current_price / (1 + price_change)

        quantity = investment_amount / past_price
        current_value = quantity * current_price

        return {
            "symbol": symbol,
            "investment_amount": investment_amount,
            "purchase_date": (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d"),
            "purchase_price": past_price,
            "current_price": current_price,
            "quantity": quantity,
            "current_value": current_value,
            "profit_loss": current_value - investment_amount,
            "return_rate": (current_value - investment_amount) / investment_amount,
            "days_held": days_ago
        }

    @staticmethod
    def generate_api_error_response(
        status_code: int = 400,
        error_name: str = "ValidationError"
    ) -> Dict[str, Any]:
        """
        API 에러 응답 생성

        Args:
            status_code: HTTP 상태 코드
            error_name: 에러 이름
        """
        error_messages = {
            400: "잘못된 요청입니다.",
            401: "인증이 필요합니다.",
            403: "권한이 없습니다.",
            404: "리소스를 찾을 수 없습니다.",
            429: "요청 한도를 초과했습니다.",
            500: "서버 내부 오류입니다.",
            502: "게이트웨이 오류입니다.",
            503: "서비스를 사용할 수 없습니다."
        }

        return {
            "error": {
                "name": error_name,
                "message": error_messages.get(status_code, "알 수 없는 오류입니다.")
            }
        }

# 편의 함수들
def create_sample_tickers(markets: List[str] = None) -> List[Dict[str, Any]]:
    """여러 마켓의 티커 데이터 생성"""
    if markets is None:
        markets = ["KRW-BTC", "KRW-ETH", "KRW-ADA"]

    return [TestDataGenerator.generate_ticker_data(market) for market in markets]

def create_price_history(
    symbol: str = "BTC",
    days: int = 30,
    trend: str = "random"
) -> List[Dict[str, Any]]:
    """가격 히스토리 데이터 생성"""
    return TestDataGenerator.generate_candle_data(
        market=f"KRW-{symbol}",
        count=days,
        trend=trend
    )