"""解决N年上半年，N年下半年的日期表述，以及N年的表述。比如：

2017年，
2017年上半年，
去年，
去年上半年，
今年，
今年下半年，
明年
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import parse_year

def year_period(func_str: str):
    """year_period(year,half_year,mask)
    
    函数参数说明：
    1. year：两种情形：指定年份，比如2017，18；还有表示与当前的相对偏移，比如-1，-3，5
    2. half_year：0表示上半年，1表示下半年
    3. mask：
        0 表示year是指定年份；
        1 表示year是相对偏移；
        2 表示不使用half_year参数，而是表示全年，而且year是准确的年份
        3 不使用half_year且year是相对偏移
    """
    params = get_params(func_str)
    if len(params) == 3:
        year_str = params[0]
        half_year = int(params[1])
        mask = int(params[2])
        return _year_period(year_str, half_year, mask)
    else:
        return None    
    
    
def _year_period(year_str: str, half_year: int, mask: int):
    if mask == 0:
        year = parse_year(year_str)
        if half_year == 0:
            start = datetime(year, 1, 1)
            end = datetime(year,6,30)
        else:
            start = datetime(year, 7, 1)
            end = datetime(year, 12, 31)
    elif mask == 1:
        year_offset = int(year_str)
        date = datetime.now() + relativedelta(years=year_offset)
        year = date.year
        
        if half_year == 0:
            start = datetime(year, 1, 1)
            end = datetime(year,6,30)
        else:
            start = datetime(year, 7, 1)
            end = datetime(year, 12, 31)
    elif mask == 2:
        year = parse_year(year_str)
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
    elif mask == 3:
        year_offset = int(year_str)
        date = datetime.now() + relativedelta(years=year_offset)
        year = date.year
        
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
    else:
        return None
    
    start_date = start.strftime('%Y%m%d')
    end_date = end.strftime('%Y%m%d')
    
    return (start_date, end_date)
