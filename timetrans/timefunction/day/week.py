"""解决和周有关的描述，比如周几，上周几，下周几，三周前，四周后
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta, weekday

from timetrans.timefunction.utils.param_utils import get_params


def week(week_expr: str):
    """week(week,weekday,mask)

    week日期函数的参数说明：
    1. week：解决周的偏移问题
    2. weekday：解决是周几的问题，0表示周一，6表示周日
    3. mask：是否处理weekday，0表示不处理weekday参数；1表示处理
    """
    params = get_params(week_expr)
    if len(params) == 3:
        week = int(params[0])
        weekday = int(params[1])
        mask = int(params[2])
        return _week(week, weekday, mask)
    return ''


def _week(week: int, week_day: int, mask: int):
    """
    1. week表示先对当前周，偏移量，可以为正可以为负；
    2. week_day表示周几，0~6
    """
    now = datetime.now()
    now += relativedelta(weeks=week)

    if mask:  # mask为1表示使用zhouji参数
        # 先将日期改为向前推的周一
        now += relativedelta(weekday=weekday(0)(-1))
        now += relativedelta(weekday=weekday(week_day))

    return now.strftime("%Y%m%d")
