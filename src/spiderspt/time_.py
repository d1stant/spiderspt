import time
from typing import Literal

import requests
from requests import Response


def timestamp_format(timestamp: int | float, format_: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化时间戳

    Args:
        timestamp (int | float): 时间戳
        format_ (str, optional): 格式化字符产格式. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: 格式化后的时间
    """
    return time.strftime(format_, time.localtime(timestamp))


def timestr_to_timestamp(time_: str, format_: str = "%Y-%m-%d %H:%M:%S") -> int:
    """格式化字符串时间转时间戳

    Args:
        time_ (str): 格式化的字符串时间
        format_ (str, optional): 字符串的格式化形式. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        int | float: 转换之后的时间戳
    """
    return round(time.mktime(time.strptime(time_, format_)))


def get_web_time(
    return_: Literal["format", "timestamp"] = "timestamp",
) -> int | str:
    """从国家授时中心获取当前时间

    Args:
        return_ (Literal["format", "timestamp"], optional): 返回格式. Defaults to "timestamp".

    Returns:
        int | str: 格式化字符串(xxxx-xx-xx xx:xx:xx)或者时间戳
    """
    url = "https://sapi.chinattas.com/time-serv"
    response: Response = requests.get(url)
    result: dict[str, str] = response.json()
    format_time: str = result["sysTime2"]
    if return_ == "timestamp":
        return timestr_to_timestamp(format_time)
    return format_time
