"""这个时间函数解决如下时间表述：
time (到|至|-) time的形式，要求time是如下一种形式：

time的形式可以是其他时间函数能够解析的形式

"""

from datetime import datetime
from dateutil.relativedelta import relativedelta


def time2time(func_str: str):
    """
    """