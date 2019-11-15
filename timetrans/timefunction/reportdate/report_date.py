"""当前函数为了支持如下形式的表述：
N年N季报，比如2017年3季报
去年年报
去年中报
前年三季报

转化结果的约定：
一季报：yyyy0331
二季报：yyyy0630
三季报：yyyy0930
年报：yyyy1231
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import parse_year


def report_date(func_str: str):
    """report_date(year,report,type)

    参数说明：
    1. year: 两种形式，一种是确定的年份，比如2018，另一种是相对偏移-1，1
    2. report: 1~4分别对应一季报到年报，0表示获取最新报告期，这个结合type=2使用
    3. type:
        0: 表示年份是确定的年份
        1: 表示年份是相对的年份
        2: 表示不再关心year参数，而是获取最新的report指定的报告期
    """
    params = get_params(func_str)
    if len(params) == 3:
        year_str = params[0]
        report = int(params[1])
        type_int = int(params[2])
        return _report_date(year_str, report, type_int)
    else:
        return ''


def _report_date(year_str: str, report: int, type: int):
    if type == 0:
        year = parse_year(year_str)
        if year == 0:
            return ''
    elif type == 1:
        year_offset = int(year_str)
        date = datetime.now() + relativedelta(years=year_offset)
        year = date.year
    elif type == 2:
        return _latest_report(report)
    else:
        return ''

    if report == 1:
        date = datetime(year, 3, 31)
    elif report == 2:
        date = datetime(year, 6, 30)
    elif report == 3:
        date = datetime(year, 9, 30)
    elif report == 4:
        date = datetime(year, 12, 31)
    else:
        return ''

    return date.strftime('%Y%m%d')


def _latest_report(report: int):
    """获取最新的报告期
    """
    now = datetime.now()

    year = now.year
    month = now.month

    report1 = 5
    report2 = 8
    report3 = 11
    report4 = 2

    if report == 0:
        if month < report1:
            date = datetime(year-1, 12, 31)
        elif month < report2:
            date = datetime(year, 3, 31)
        elif month < report3:
            date = datetime(year, 6, 30)
        else:
            date = datetime(year, 9, 30)
    elif report == 1:
        if month < report1:
            year -= 1
        date = datetime(year, 3, 31)
    elif report == 2:
        if month < report2:
            year -= 1
        date = datetime(year, 6, 30)
    elif report == 3:
        if month < report3:
            year -= 1
        date = datetime(year, 9, 30)
    elif report == 4:
        year -= 1
        if month < report4:
            year -= 2
        date = datetime(year, 12, 31)
    else:
        return ''

    return date.strftime('%Y%m%d')
