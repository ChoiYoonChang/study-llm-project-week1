# 암호화폐 분석 프로젝트 Class Diagram

## 📊 전체 시스템 클래스 구조

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Main Module                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                main.py                                     │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                          MainApplication                               │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + print_welcome_message(): void                                        │ │
│ │ + show_menu(): void                                                     │ │
│ │ + main(): void                                                          │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ uses
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Configuration Module                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                             config/settings.py                            │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                              Settings                                   │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + UPBIT_API_BASE_URL: str                                               │ │
│ │ + API_ENDPOINTS: Dict[str, str]                                         │ │
│ │ + REQUEST_TIMEOUT: int                                                  │ │
│ │ + MAX_RETRIES: int                                                      │ │
│ │ + CURRENCY_FORMAT: str                                                  │ │
│ │ + PERCENTAGE_FORMAT: str                                                │ │
│ │ + DATETIME_FORMAT: str                                                  │ │
│ │ + DEFAULT_CRYPTOS: List[str]                                            │ │
│ │ + DEFAULT_PRICE_CHANGE_THRESHOLD: float                                 │ │
│ │ + DEFAULT_MONITORING_CYCLES: int                                        │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ imports
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Utility Modules                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                           utils/api_client.py                              │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                              ApiClient                                  │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + make_api_request(url: str, params: Dict): Optional[Dict]              │ │
│ │ + get_current_prices(markets: List[str]): Dict[str, float]              │ │
│ │ + get_single_price(market: str): Optional[float]                        │ │
│ │ + get_historical_data(market: str, count: int): Optional[List[Dict]]     │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│                           utils/date_utils.py                              │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                             DateUtils                                   │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + get_current_time(): str                                               │ │
│ │ + get_current_datetime(): str                                           │ │
│ │ + get_date_days_ago(days: int): datetime                                │ │
│ │ + format_date(date_obj: datetime, format_str: str): str                 │ │
│ │ + parse_upbit_datetime(upbit_date_str: str): datetime                   │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│                          utils/format_utils.py                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                            FormatUtils                                  │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + format_currency(amount: float, currency: str): str                    │ │
│ │ + format_percentage(value: float, decimal_places: int): str             │ │
│ │ + format_crypto_amount(amount: float, decimal_places: int): str         │ │
│ │ + format_price_change(current: float, previous: float): tuple           │ │
│ │ + create_table_header(columns: list, widths: list): str                 │ │
│ │ + create_table_row(values: list, widths: list, alignments: list): str   │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ uses
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Business Logic Modules                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                        src/portfolio_analyzer.py                           │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                         PortfolioAnalyzer                               │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ - portfolio: Dict[str, float]                                           │ │
│ │ - analysis_result: Dict[str, Any]                                       │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + get_current_prices_api(markets: List[str]): Dict[str, float]          │ │
│ │ + validate_portfolio(portfolio: Dict[str, float]): bool                 │ │
│ │ + analyze_portfolio(portfolio: Dict[str, float]): Dict[str, Any]        │ │
│ │ + print_portfolio_summary(analysis_result: Dict[str, Any]): void        │ │
│ │ + print_portfolio_table(analysis_result: Dict[str, Any]): void          │ │
│ │ + get_sample_portfolio(): Dict[str, float]                              │ │
│ │ + get_custom_portfolio(): Dict[str, float]                              │ │
│ │ + run_portfolio_analyzer(): void                                        │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│                           src/price_alert.py                               │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                            PriceAlert                                   │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ - market: str                                                           │ │
│ │ - target_high: float                                                    │ │
│ │ - target_low: float                                                     │ │
│ │ - monitoring_cycles: int                                                │ │
│ │ - monitoring_interval: int                                              │ │
│ │ - alerts_triggered: int                                                 │ │
│ │ - monitoring_data: List[Dict]                                           │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + get_single_price_api(market: str): Optional[float]                    │ │
│ │ + calculate_target_prices(current_price: float, threshold: float): Tuple│ │
│ │ + validate_market_code(market: str): bool                               │ │
│ │ + check_price_alert_condition(current: float, high: float, low: float)  │ │
│ │ + display_monitoring_info(...): void                                    │ │
│ │ + display_monitoring_status(...): void                                  │ │
│ │ + price_alert_system(...): Dict[str, Any]                              │ │
│ │ + get_user_alert_settings(): Optional[Dict[str, Any]]                   │ │
│ │ + get_preset_alert_settings(): Dict[str, Any]                           │ │
│ │ + run_price_alert(): void                                               │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│                        src/return_calculator.py                            │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                          ReturnCalculator                               │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ - market: str                                                           │ │
│ │ - investment_amount: float                                              │ │
│ │ - investment_date: str                                                  │ │
│ │ - investment_price: float                                               │ │
│ │ - current_price: float                                                  │ │
│ │ - purchase_quantity: float                                              │ │
│ │ - current_value: float                                                  │ │
│ │ - profit_loss: float                                                    │ │
│ │ - return_rate: float                                                    │ │
│ │ - annual_return_rate: float                                             │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + get_historical_data_api(market: str, days: int): Optional[List[Dict]] │ │
│ │ + find_investment_date_price(data: List[Dict], days: int): Optional[Tuple]│ │
│ │ + calculate_investment_return(market: str, days: int, amount: float)    │ │
│ │ + calculate_annual_return_rate(return_rate: float, days: int): float    │ │
│ │ + print_investment_result(result: Dict[str, Any]): void                 │ │
│ │ + get_user_investment_settings(): Optional[Dict[str, Any]]              │ │
│ │ + get_preset_investment_scenarios(): List[Dict[str, Any]]               │ │
│ │ + compare_multiple_scenarios(scenarios: List[Dict[str, Any]]): void     │ │
│ │ + run_return_calculator(): void                                         │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ 모듈 간 관계 다이어그램

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   main.py       │────▶│ PortfolioAnalyzer│────▶│   ApiClient     │
│                 │     │                 │     │                 │
│                 │     └─────────────────┘     └─────────────────┘
│                 │              │                       │
│                 │              ▼                       │
│                 │     ┌─────────────────┐              │
│                 │────▶│   PriceAlert    │──────────────┘
│                 │     │                 │
│                 │     └─────────────────┘
│                 │              │
│                 │              ▼
│                 │     ┌─────────────────┐
│                 │────▶│ ReturnCalculator│──────────────┐
│                 │     │                 │              │
└─────────────────┘     └─────────────────┘              │
         │                        │                       │
         │                        ▼                       ▼
         │               ┌─────────────────┐     ┌─────────────────┐
         │               │   DateUtils     │     │   FormatUtils   │
         │               │                 │     │                 │
         │               └─────────────────┘     └─────────────────┘
         │                        │                       │
         ▼                        │                       │
┌─────────────────┐               │                       │
│    Settings     │◄──────────────┼───────────────────────┘
│                 │               │
└─────────────────┘               │
         ▲                        │
         │                        │
         └────────────────────────┘
```

---

## 📊 데이터 모델 클래스 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Data Models                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                           Portfolio                                     │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + market: str                     # 마켓 코드 (예: "KRW-BTC")           │ │
│ │ + quantity: float                 # 보유 수량                            │ │
│ │ + current_price: float            # 현재가                              │ │
│ │ + value: float                    # 현재 가치 (수량 × 현재가)            │ │
│ │ + percentage: float               # 포트폴리오 내 비중                    │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                         PortfolioAnalysis                              │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + total_value: float              # 전체 포트폴리오 가치                 │ │
│ │ + analysis: List[Portfolio]       # 개별 암호화폐 분석 결과              │ │
│ │ + success: bool                   # 분석 성공 여부                       │ │
│ │ + error_message: str              # 오류 메시지                         │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                          AlertCondition                                │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + market: str                     # 모니터링 대상 마켓                  │ │
│ │ + target_high: float              # 상한가 목표                         │ │
│ │ + target_low: float               # 하한가 목표                         │ │
│ │ + current_price: float            # 현재가                              │ │
│ │ + alert_triggered: bool           # 알림 발생 여부                       │ │
│ │ + alert_type: str                 # 알림 타입 ("high", "low", "normal") │ │
│ │ + message: str                    # 알림 메시지                         │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                         MonitoringRecord                               │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + cycle: int                      # 모니터링 사이클 번호                 │ │
│ │ + time: str                       # 조회 시간                           │ │
│ │ + price: float                    # 조회된 가격                         │ │
│ │ + alert_triggered: bool           # 알림 발생 여부                       │ │
│ │ + alert_type: str                 # 알림 타입                           │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                         MonitoringResult                               │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + success: bool                   # 모니터링 성공 여부                   │ │
│ │ + error_message: str              # 오류 메시지                         │ │
│ │ + alerts_triggered: int           # 총 알림 발생 횟수                    │ │
│ │ + final_price: Optional[float]    # 최종 가격                           │ │
│ │ + monitoring_data: List[MonitoringRecord] # 모니터링 기록                │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                        InvestmentScenario                              │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + market: str                     # 투자 대상 마켓                       │ │
│ │ + days_ago: int                   # 투자 시점 (며칠 전)                  │ │
│ │ + investment_amount: float        # 투자 금액                           │ │
│ │ + investment_date: str            # 투자 일자                           │ │
│ │ + investment_price: float         # 투자 시점 가격                       │ │
│ │ + current_price: float            # 현재 가격                           │ │
│ │ + purchase_quantity: float        # 구매 수량                           │ │
│ │ + current_value: float            # 현재 가치                           │ │
│ │ + profit_loss: float              # 손익                               │ │
│ │ + return_rate: float              # 수익률 (%)                          │ │
│ │ + annual_return_rate: float       # 연간 수익률 (%)                      │ │
│ │ + is_profit: bool                 # 수익 여부                           │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                        InvestmentResult                                │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + success: bool                   # 계산 성공 여부                       │ │
│ │ + error_message: str              # 오류 메시지                         │ │
│ │ + scenario: InvestmentScenario    # 투자 시나리오 결과                   │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                         HistoricalData                                 │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + market: str                     # 마켓 코드                           │ │
│ │ + candle_date_time_kst: str       # 일봉 날짜/시간 (KST)                │ │
│ │ + opening_price: float            # 시가                               │ │
│ │ + high_price: float               # 고가                               │ │
│ │ + low_price: float                # 저가                               │ │
│ │ + trade_price: float              # 종가 (현재가)                       │ │
│ │ + candle_acc_trade_volume: float  # 누적 거래량                         │ │
│ │ + candle_acc_trade_price: float   # 누적 거래대금                       │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 인터페이스 및 추상 클래스 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Abstract Classes & Interfaces                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                      <<interface>>                                      │ │
│ │                       DataValidator                                     │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + validate(data: Any): bool                                             │ │
│ │ + get_error_message(): str                                              │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                   ▲                                         │
│                                   │                                         │
│                    ┌──────────────┼──────────────┐                          │
│                    │              │              │                          │
│                    ▼              ▼              ▼                          │
│ ┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐         │
│ │ PortfolioValidator  │ │ MarketValidator │ │ InvestmentValidator │         │
│ ├─────────────────────┤ ├─────────────────┤ ├─────────────────────┤         │
│ │ + validate(): bool  │ │ + validate(): bool │ │ + validate(): bool  │         │
│ └─────────────────────┘ └─────────────────┘ └─────────────────────┘         │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                      <<interface>>                                      │ │
│ │                       ApiConnector                                      │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + connect(): bool                                                       │ │
│ │ + fetch_data(params: Dict): Optional[Dict]                              │ │
│ │ + handle_error(error: Exception): void                                  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                   ▲                                         │
│                                   │                                         │
│                                   │                                         │
│                                   ▼                                         │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                        UpbitApiConnector                                │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ - base_url: str                                                         │ │
│ │ - timeout: int                                                          │ │
│ │ - max_retries: int                                                      │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + connect(): bool                                                       │ │
│ │ + fetch_current_prices(markets: List[str]): Dict[str, float]            │ │
│ │ + fetch_historical_data(market: str, days: int): List[Dict]             │ │
│ │ + fetch_single_price(market: str): float                                │ │
│ │ + handle_error(error: Exception): void                                  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                      <<interface>>                                      │ │
│ │                         Formatter                                       │ │
│ ├─────────────────────────────────────────────────────────────────────────┤ │
│ │ + format(data: Any): str                                                │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                   ▲                                         │
│                                   │                                         │
│                   ┌───────────────┼───────────────┐                         │
│                   │               │               │                         │
│                   ▼               ▼               ▼                         │
│ ┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐         │
│ │  CurrencyFormatter  │ │ PercentFormatter│ │   TableFormatter    │         │
│ ├─────────────────────┤ ├─────────────────┤ ├─────────────────────┤         │
│ │ + format(): str     │ │ + format(): str │ │ + format(): str     │         │
│ └─────────────────────┘ └─────────────────┘ └─────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 상속 관계 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Inheritance Hierarchy                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                     ┌─────────────────────────────┐                         │
│                     │      <<abstract>>           │                         │
│                     │      BaseAnalyzer           │                         │
│                     ├─────────────────────────────┤                         │
│                     │ # data: Dict[str, Any]      │                         │
│                     │ # result: Dict[str, Any]    │                         │
│                     ├─────────────────────────────┤                         │
│                     │ + validate_input(): bool    │                         │
│                     │ + process_data(): void      │                         │
│                     │ + generate_result(): Dict   │                         │
│                     │ + display_result(): void    │                         │
│                     │ + run(): void              │                         │
│                     └─────────────────────────────┘                         │
│                                   ▲                                         │
│                     ┌─────────────┼─────────────┐                           │
│                     │             │             │                           │
│                     ▼             ▼             ▼                           │
│ ┌─────────────────────────┐ ┌─────────────┐ ┌─────────────────────────┐     │
│ │   PortfolioAnalyzer     │ │ PriceAlert  │ │   ReturnCalculator      │     │
│ ├─────────────────────────┤ ├─────────────┤ ├─────────────────────────┤     │
│ │ - portfolio: Dict       │ │ - market: str│ │ - scenarios: List       │     │
│ │ - prices: Dict          │ │ - targets: Dict│ │ - historical: List      │     │
│ ├─────────────────────────┤ ├─────────────┤ ├─────────────────────────┤     │
│ │ + validate_input(): bool│ │ + validate_input()│ │ + validate_input(): bool│     │
│ │ + process_data(): void  │ │ + process_data()│ │ + process_data(): void  │     │
│ │ + generate_result(): Dict│ │ + generate_result()│ │ + generate_result(): Dict│     │
│ │ + display_result(): void│ │ + display_result()│ │ + display_result(): void│     │
│ │ + calculate_values()    │ │ + monitor_price()│ │ + calculate_returns()   │     │
│ │ + calculate_percentages()│ │ + check_alerts()│ │ + compare_scenarios()   │     │
│ └─────────────────────────┘ └─────────────┘ └─────────────────────────┘     │
│                                                                             │
│                     ┌─────────────────────────────┐                         │
│                     │      <<abstract>>           │                         │
│                     │      BaseException          │                         │
│                     ├─────────────────────────────┤                         │
│                     │ + message: str              │                         │
│                     │ + error_code: int           │                         │
│                     ├─────────────────────────────┤                         │
│                     │ + __init__(message: str)    │                         │
│                     │ + __str__(): str            │                         │
│                     └─────────────────────────────┘                         │
│                                   ▲                                         │
│                 ┌─────────────────┼─────────────────┐                       │
│                 │                 │                 │                       │
│                 ▼                 ▼                 ▼                       │
│ ┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐         │
│ │   ApiException      │ │ ValidationError │ │  CalculationError   │         │
│ ├─────────────────────┤ ├─────────────────┤ ├─────────────────────┤         │
│ │ + endpoint: str     │ │ + field: str    │ │ + operation: str    │         │
│ │ + status_code: int  │ │ + value: Any    │ │ + input_data: Dict  │         │
│ └─────────────────────┘ └─────────────────┘ └─────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 의존성 관계 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Dependency Graph                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     ┌─────────────┐                                                         │
│     │   main.py   │                                                         │
│     └──────┬──────┘                                                         │
│            │ depends on                                                     │
│            ▼                                                                │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │                   Business Layer                       │             │
│     │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │             │
│     │  │ Portfolio   │ │ PriceAlert  │ │ ReturnCalculator│   │             │
│     │  │ Analyzer    │ │             │ │                 │   │             │
│     │  └─────────────┘ └─────────────┘ └─────────────────┘   │             │
│     └─────────────────────┬───────────────────────────────────┘             │
│                           │ depends on                                      │
│                           ▼                                                 │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │                   Service Layer                        │             │
│     │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │             │
│     │  │ ApiClient   │ │ DateUtils   │ │ FormatUtils     │   │             │
│     │  │             │ │             │ │                 │   │             │
│     │  └─────────────┘ └─────────────┘ └─────────────────┘   │             │
│     └─────────────────────┬───────────────────────────────────┘             │
│                           │ depends on                                      │
│                           ▼                                                 │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │                Infrastructure Layer                    │             │
│     │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │             │
│     │  │ Settings    │ │ HTTP Client │ │ System Libraries│   │             │
│     │  │ (config)    │ │ (requests)  │ │ (datetime, etc) │   │             │
│     │  └─────────────┘ └─────────────┘ └─────────────────┘   │             │
│     └─────────────────────┬───────────────────────────────────┘             │
│                           │ depends on                                      │
│                           ▼                                                 │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │                 External Services                      │             │
│     │              ┌─────────────────┐                       │             │
│     │              │   업비트 API     │                       │             │
│     │              │  (upbit.com)    │                       │             │
│     │              └─────────────────┘                       │             │
│     └─────────────────────────────────────────────────────────┘             │
│                                                                             │
│  Data Flow Direction: Top ──→ Bottom                                       │
│  Control Flow Direction: Bottom ──→ Top                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 패키지 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Package Structure                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  week1-python-project/                                                      │
│  │                                                                          │
│  ├── main.py                           # Entry Point                        │
│  │                                                                          │
│  ├── config/                           # Configuration Package              │
│  │   ├── __init__.py                                                        │
│  │   └── settings.py                   # Global Settings                    │
│  │                                                                          │
│  ├── utils/                            # Utility Package                    │
│  │   ├── __init__.py                                                        │
│  │   ├── api_client.py                 # API Communication                  │
│  │   ├── date_utils.py                 # Date/Time Operations               │
│  │   └── format_utils.py               # Data Formatting                    │
│  │                                                                          │
│  ├── src/                              # Business Logic Package             │
│  │   ├── __init__.py                                                        │
│  │   ├── portfolio_analyzer.py         # Phase 2 Implementation             │
│  │   ├── price_alert.py                # Phase 3 Implementation             │
│  │   └── return_calculator.py          # Phase 4 Implementation             │
│  │                                                                          │
│  ├── tests/                            # Test Package                       │
│  │   ├── __init__.py                                                        │
│  │   ├── test_api_client.py                                                 │
│  │   ├── test_portfolio_analyzer.py                                         │
│  │   ├── test_price_alert.py                                                │
│  │   └── test_return_calculator.py                                          │
│  │                                                                          │
│  └── docs/                             # Documentation Package              │
│      ├── phase1-project-setup.md                                            │
│      ├── phase2-portfolio-analyzer.md                                       │
│      ├── phase3-price-alert-system.md                                       │
│      ├── phase4-return-calculator.md                                        │
│      ├── flowchart.md                                                       │
│      ├── sequence-diagram.md                                                │
│      └── class-diagram.md                                                   │
│                                                                             │
│ Package Dependencies:                                                       │
│ ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                     │
│ │    main     │────▶│     src     │────▶│    utils    │                     │
│ └─────────────┘     └─────────────┘     └─────────────┘                     │
│                              │                 │                           │
│                              ▼                 ▼                           │
│                     ┌─────────────┐     ┌─────────────┐                     │
│                     │   config    │     │   tests     │                     │
│                     └─────────────┘     └─────────────┘                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

이 클래스 다이어그램들은 프로젝트의 객체지향적 구조, 모듈 간 관계, 데이터 모델, 그리고 전체적인 아키텍처를 보여줍니다.