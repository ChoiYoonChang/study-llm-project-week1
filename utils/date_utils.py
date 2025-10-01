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