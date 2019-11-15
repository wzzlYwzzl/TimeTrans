"""解决如下类型的日期表述：
今年一季度；
2017年三季度；
明年一季度；
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import parse_year


def season_period(func_str: str):
    """season_period(year,season,mask)

    参数说明：
    1. year：两种形式，确定的年份，比如2017，19；或者相对偏移-1，4
    2. season：1~4分别表示4个季度
    3. mask
        0 表示year是确定年份；
        1 表示year是相对年份；
    """
    params = get_params(func_str)
    if len(params) == 3:
        year_str = params[0].strip()
        season = int(params[1])
        mask = int(params[2])
        return _season_period(year_str, season, mask)
    else:
        return None


def _season_period(year_str: str, season: int, mask: int):
    if mask == 0:
        year = parse_year(year_str)
    else:
        year_offset = int(year_str)
        date = datetime.now() + relativedelta(years=year_offset)
        year = date.year

    if season == 1:
        start = datetime(year, 1, 1)
        end = datetime(year, 3, 31)
    elif season == 2:
        start = datetime(year, 4, 1)
        end = datetime(year, 6, 30)
    elif season == 3:
        start = datetime(year, 7, 1)
        end = datetime(year, 9, 30)
    else:
        start = datetime(year, 10, 1)
        end = datetime(year, 12, 31)

    start_date = start.strftime('%Y%m%d')
    end_date = end.strftime('%Y%m%d')
    return (start_date, end_date)
