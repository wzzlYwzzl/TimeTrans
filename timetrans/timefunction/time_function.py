from timetrans.timefunction.day.n2time_day import n2time_day
from timetrans.timefunction.day.week import week
from timetrans.timefunction.day.year_month_day import year_month_day

from timetrans.timefunction.period.period import period
from timetrans.timefunction.period.year_period import year_period
from timetrans.timefunction.period.season_period import season_period
from timetrans.timefunction.period.month_period import month_period
from timetrans.timefunction.period.n2time_period import n2time_period

from timetrans.timefunction.reportdate.report_date import report_date

from timetrans.timefunction.utils import param_utils

# 函数名与函数对象的对应关系
func_map = {
    'n2time_day': n2time_day,
    'week': week,
    'year_month_day': year_month_day,
    'period': period,
    'year_period': year_period,
    'season_period': season_period,
    'month_period': month_period,
    'n2time_period': n2time_period,
    'report_date': report_date
}


def exec_function(func_str: str):
    """执行时间函数返回结果
    """
    func_name = param_utils.get_time_func_name(func_str)
    if func_name in func_map:
        time_func = func_map[func_name]
        return time_func(func_str)
    else:
        return None