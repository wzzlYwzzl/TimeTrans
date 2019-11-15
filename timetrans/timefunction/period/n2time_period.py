"""解决如下场景的时间表示：

N是一个数字，但是这个数字其实是一个日期，比如2018，20191231，201807。

按照如下约定获取时间区间：
2017 -> (20170101,20171231)
201708 -> (20170801,20170831)
20170812 -> (20170812,20170812)
"""

import calendar
from datetime import datetime

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import parse_year


def n2time_period(func_str: str):
    """n2time_period(N)
    """
    params = get_params(func_str)
    if len(params) == 1:
        return _n2time_period(params[0])
    else:
        return None


def _n2time_period(date_str: str):
    if len(date_str) == 8:  # 按照yyyymmdd形式尝试解析
        year = parse_year(date_str[0:4])
        if year == 0:  # 表示年份不合法
            return None

        month = int(date_str[4:6])
        if month < 1 or month > 12:  # 表示月份不合法
            return None

        day = int(date_str[6:8])
        _, max_day = calendar.monthrange(year, month)
        if day <= 0 or day > max_day:  # 表示日不合法
            return None

        return (date_str, date_str)
    elif len(date_str) == 7:  # 尝试按照yyyymmd和yyyymdd的形式解析
        year = parse_year(date_str[0:4])
        if year == 0:
            return None

        month = int(date_str[4:6])
        day_str = date_str[6:7]
        if month < 1 or month > 12:
            month = int(date_str[4:5])
            day_str = date_str[5:7]
            if month < 1:
                return None

        day = int(day_str)
        _, max_day = calendar.monthrange(year, month)
        if day <= 0 or day > max_day:  # 表示日不合法
            return None

        date = datetime(year, month, day).strftime('%Y%m%d')
        return (date, date)

    elif len(date_str) == 6:  # 按照yyyymm去解析
        year = parse_year(date_str[0:4])
        if year == 0:
            return None

        month = int(date_str[4:6])
        if month < 1 or month > 12:
            return None

        _, max_day = calendar.monthrange(year, month)

        start_date = datetime(year, month, 1).strftime('%Y%m%d')
        end_date = datetime(year, month, max_day).strftime('%Y%m%d')
        return (start_date, end_date)

    elif len(date_str) == 4:  # 按照yyyy去解析
        year = parse_year(date_str[0:4])
        if year == 0:
            return ''

        start_date = datetime(year, 1, 1).strftime('%Y%m%d')
        end_date = datetime(year, 12, 31).strftime('%Y%m%d')
        return (start_date, end_date)
    else:
        return None
