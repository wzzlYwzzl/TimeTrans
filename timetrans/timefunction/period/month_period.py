"""解决如下时间的表述：
2017年3月，
去年5月，
2018年5月上半月，
8月下半月
"""
import calendar

from datetime import datetime
from dateutil.relativedelta import relativedelta

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import parse_year

def month_period(func_str: str):
    """month_period(year,month,year_type,month_type)
    
    参数说明：
    1. year：确定的年份比如2018，19；或者年份的偏移；
    2. month：月份1~12，分别表示1月到12月
    3. year_type: 0 表示year是确定的年，1表示year是偏移；
    4. month_type: 0 表示是整个月，1表示上半月，2表示下半月
    """
    params = get_params(func_str)
    if len(params) == 4:
        year_str = params[0]
        month = int(params[1])
        year_type = int(params[2])
        month_type = int(params[3])
        return _month_period(year_str, month, year_type, month_type)
    else:
        return None


def _month_period(year_str: str, month: int, year_type: int, month_type: int):
    if year_type == 0:
        year = parse_year(year_str)
    else:
        year_offset = int(year_str)
        date = datetime.now() + relativedelta(years=year_offset)
        year = date.year
        
    if month_type == 0:
        day1 = 1
        _, day2 = calendar.monthrange(year, month)
    elif month_type == 1:
        day1 = 1
        day2 = 15
    else:
        day1 = 15
        _, day2 = calendar.monthrange(year, month)
        
    start_date = datetime(year, month, day1).strftime('%Y%m%d')
    end_date = datetime(year, month, day2).strftime('%Y%m%d')
    
    return (start_date, end_date)