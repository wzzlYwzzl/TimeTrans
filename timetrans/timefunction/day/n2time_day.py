"""解决如下场景的时间表示：

N是一个数字，但是这个数字其实是一个日期，比如2018，20191231，201807。

由于这里的翻译是将其翻译为单个日期，所以有如下约定：
2017     -> 20171231
201706   -> 20170630
20170612 -> 20170612

"""

import calendar
from datetime import datetime

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import parse_year


def n2time_day(func_str: str):
    """n2time_day(N)
    """
    params = get_params(func_str)
    if len(params) == 1:
        return _n2time_day(params[0])
    else:
        return ''


def _n2time_day(date_str: str):
    if len(date_str) == 8:  # 按照yyyymmdd形式尝试解析
        year = parse_year(date_str[0:4])
        if year == 0:  # 表示年份不合法
            return ''

        month = int(date_str[4:6])
        if month < 1 or month > 12:  # 表示月份不合法
            return ''

        day = int(date_str[6:8])
        _, max_day = calendar.monthrange(year, month)
        if day <= 0 or day > max_day:  # 表示日不合法
            return ''

        return date_str
    elif len(date_str) == 7:  # 尝试按照yyyymmd和yyyymdd的形式解析
        year = parse_year(date_str[0:4])
        if year == 0:
            return ''

        month = int(date_str[4:6])
        day_str = date_str[6:7]
        if month < 1 or month > 12:
            month = int(date_str[4:5])
            day_str = date_str[5:7]
            if month < 1:
                return ''

        day = int(day_str)
        _, max_day = calendar.monthrange(year, month)
        if day <= 0 or day > max_day:  # 表示日不合法
            return ''

        return datetime(year, month, day).strftime('%Y%m%d')
    elif len(date_str) == 6:  # 按照yyyymm去解析
        year = parse_year(date_str[0:4])
        if year == 0:
            return ''

        month = int(date_str[4:6])
        if month < 1 or month > 12:
            return ''

        _, day = calendar.monthrange(year, month)
        return datetime(year, month, day).strftime('%Y%m%d')
    elif len(date_str) == 4:  # 按照yyyy去解析
        year = parse_year(date_str[0:4])
        if year == 0:
            return ''
        return datetime(year, 12, 31).strftime('%Y%m%d')
    else:
        return ''
