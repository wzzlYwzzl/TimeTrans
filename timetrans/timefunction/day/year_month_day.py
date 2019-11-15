"""单个日期的表示函数
"""
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import parse_year


def year_month_day(func_str: str):
    """将 year_month_day(year,month,day,mask)函数
    解析成"yyyyMMdd"格式的日期字符串。

    解析失败则返回''空字符串
    """
    params = get_params(func_str)
    if len(params) >= 4:
        year = params[0]
        month = int(params[1])
        day = int(params[2])
        mask = int(params[3])
        return _year_month_day(year, month, day, mask)
    else:
        return ''


def _year_month_day(year: str, month: int, day: int, mask: int):
    """mask是***三位的掩码，分别用于说明year、month、day是否是相对现在的偏移。
    如果相应位是1，则表示是，为0则表示不是。
    """
    now = datetime.now()

    if mask & 4:  # 表示最后四位二进制是1xxx
        years = int(year)
        rela = relativedelta(years=years)
        now += rela
    else:
        real_year = parse_year(year)
        if real_year: # 解析的real_year不是0
            rela = relativedelta(year=real_year)
            now += rela
        
    if mask & 2:
        rela = relativedelta(months=month)
        now += rela
    else:
        if month <= 12 and month > 0:
            rela = relativedelta(month=month)
            now += rela
            
    if mask & 1:
        rela = relativedelta(days=day)
        now += rela
    else:
        _, valid_days = calendar.monthrange(now.year, now.month)
        if day <= valid_days:
            rela = relativedelta(day=day)
            now += rela
            
    return now.strftime("%Y%m%d")