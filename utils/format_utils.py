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