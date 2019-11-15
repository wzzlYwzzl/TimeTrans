"""年，半年，季度，月，周，天都是时间单位，分别对应的一定天数的时长。

这里的period函数解决的就是以这些单位为相对偏移的日期表述，比如：
N天内，
N周内，
连续N周，
上个月，
当月，
上季度，
本季度，
下季度，
未来三季度，
半年内，
近N年，
去年，
明年，
今年以来，
"""

import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, SU

from timetrans.timefunction.utils.param_utils import get_params
from timetrans.timefunction.utils.time_utils import get_season


def period(period_func: str):
    params = get_params(period_func)
    if len(params) == 3:
        offset = int(params[0])
        time_type = int(params[1])
        compute_type = int(params[2])
        return _period(offset, time_type, compute_type)
    else:
        return ''


def yyyymmdd(datetime):
    return datetime.strftime('%Y%m%d')


def _period(offset: int, time_type: int, compute_type: int):
    """参数说明：
    1. offset
    时间的偏移量，正表示向后偏移，负表示向前偏移。需要注意的是：0表示的是本*，比如
    本周，本月，本季度，本年。

    2. time_type
    表示用什么时间单位，定义如下：
    0 表示天；
    1 表示周；
    2 表示月；
    3 表示季度；
    4 表示半年
    5 表示年；

    3. compute_type
    表示区间的计算逻辑。

    注意：这个compute_type会因为time_type的不同而有所差异，所以具体的含义需要参考具体的计算函数的说明。

    0 表示正常前后偏移，比如近一周，近一个月，近N季度，近几年，只是在相应的时间单位上做加减法即可。
    1 当时间偏移到某个时间区间后，取相应区间的首日作为区间日期的一部分，和当前时间组成区间。比如：自去年，去年以来，
        上半年；
    2 当时间偏移到某个时间区间后，取相应区间的末尾作为区间日期的一部分，这种情形主要用在日期后推时有用。
    3 表示取某个区间日区间内起始、截止日期作为区间日期的起始和截止。比如上个月、去年、下月、上周、大前年等等
    4 在类别是季度时，会有4这种类型。比如前三个季度，表示的前面三个季度的起始和截止
    返回的是一个tuple(start_date,end_date)，如果解析失败，返回None
    """
    if time_type == 0:
        return _day(offset, compute_type)
    elif time_type == 1:
        return _week(offset, compute_type)
    elif time_type == 2:
        return _month(offset, compute_type)
    elif time_type == 3:
        return _season(offset, compute_type)
    elif time_type == 4:
        return _half_year(offset, compute_type)
    elif time_type == 5:
        return _year(offset, compute_type)
    else:
        return None


def _day(offset: int, compute_type: int):
    """compute_type参数说明：
    0 表示直接使用offset，比如近三天，那么就直接偏移计算就可以了；
    1 表示偏移的日期是周一到周五，不包括周六和周日。在金融场景，指的是
        交易日，比如近三个交易日。需要保证这个区间内的日期必须是周一到周五
        的有效日期个数符合这个offset。
    """
    now = datetime.now()
    if compute_type == 0:
        other = now + relativedelta(days=offset)
    else:
        weekday = now.weekday()
        if offset < 0:
            base = int((- offset) / 5) * 7
            left = (-offset) % 5

            if weekday - 4 > 0:  # 当前日期是周六或周日
                left += weekday - 4
            elif weekday + 1 < left:  # 当前日期不是周六和周日，但是移动left天之后是经过周六和周日
                left += left - 1 - weekday
            other = now + relativedelta(days=-(base + left))
        else:
            base = int(offset / 5) * 7
            left = offset % 5

            if weekday - 4 > 0:  # 当前是周六或周日
                left += 7 - weekday
            elif left + weekday >= 5:  # 表示移动后经过了周六和周日
                left += 7 - (left + weekday)

            other = now + relativedelta(days=(base + left))

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)
    if offset > 0:
        return (now_date, other_date)
    else:
        return (other_date, now_date)


def _week(offset: int, compute_type: int):
    if compute_type == 0:
        return _week0(offset)
    elif compute_type == 1:
        return _week1(offset)
    elif compute_type == 2:
        return _week2(offset)
    elif compute_type == 3:
        return _week3(offset)
    else:
        return None


def _week0(offset):
    """正常偏移，以当前日期为起始，偏移前后offset个week
    """
    rela = relativedelta(weeks=offset)

    now = datetime.now()
    other = now + rela

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)
    if offset > 0:
        return (now_date, other_date)
    else:
        return (other_date, now_date)


def _week1(offset):
    """经过offset偏移之后，会进入到一个week内，取该week的周一作为区间日期的一部分，与now构成
    区间日期返回
    """
    now = datetime.now()
    rela = relativedelta(weeks=offset)

    other = now + rela
    other += relativedelta(weekday=MO(-1))  # 返回当前周的周一

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if now < other:
        return (now_date, other_date)
    else:
        return (other_date, now_date)


def _week2(offset):
    """与_week1函数相对应，这里返回offset之后的区间的最后一天，也就是"周日"作为区间的另一个日期
    """
    now = datetime.now()
    rela = relativedelta(weeks=offset)

    other = now + rela
    other += relativedelta(weekday=SU(1))  # 返回当前周的周一

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if now < other:
        return (now_date, other_date)
    else:
        return (other_date, now_date)


def _week3(offset):
    """根据offset跳转到相应区间之后，取区间内的周一作为起始日期，周日作为截止日期
    """
    now = datetime.now()
    rela_1 = relativedelta(weeks=offset, weekday=MO(-1))
    rela_2 = relativedelta(weeks=offset, weekday=SU(1))

    start = now + rela_1
    end = now + rela_2

    start_date = yyyymmdd(start)
    end_date = yyyymmdd(end)

    return (start_date, end_date)


def _month(offset: int, compute_type: int):
    if compute_type == 0:
        return _month0(offset)
    elif compute_type == 1:
        return _month1(offset)
    elif compute_type == 2:
        return _month2(offset)
    elif compute_type == 3:
        return _month3(offset)
    else:
        return None


def _month0(offset):
    """常规计算与now偏移的日期
    """
    now = datetime.now()

    rela = relativedelta(months=offset)
    other = now + rela

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if offset < 0:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _month1(offset):
    """按月offset之后，取区间的起始日期作为区间的一个日期和now构成区间日期。
    """
    now = datetime.now()
    rela = relativedelta(months=offset, day=1)

    other = now + rela

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if now > other:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _month2(offset):
    now = datetime.now()
    rela = relativedelta(months=offset)

    other = now + rela

    _, month_days = calendar.monthrange(other.year, other.month)
    other = other + relativedelta(day=month_days)

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if now > other:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _month3(offset):
    """返回偏移量内的起始日期和截止日期作为区间的开始和截止
    """
    now = datetime.now()
    the_month = now + relativedelta(months=offset)

    start = the_month + relativedelta(day=1)

    _, month_days = calendar.monthrange(the_month.year, the_month.month)
    end = the_month + relativedelta(day=month_days)

    start_date = yyyymmdd(start)
    end_date = yyyymmdd(end)

    return (start_date, end_date)


def _season(offset: int, compute_type: int):
    if compute_type == 0:
        return _season0(offset)
    elif compute_type == 1:
        return _season1(offset)
    elif compute_type == 2:
        return _season2(offset)
    elif compute_type == 3:
        return _season3(offset)
    elif compute_type == 4:
        return _season4(offset)
    else:
        return None


def _season0(offset):
    now = datetime.now()

    # 将季度直接理解为三个月来处理
    offset *= 3
    other = now + relativedelta(months=offset)

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if offset < 0:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _season1(offset):
    now = datetime.now()

    other = now + relativedelta(months=offset * 3)
    season = get_season(other.month)
    start_month = (season - 1) * 3 + 1
    other += relativedelta(month=start_month, day=1)

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if now > other:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _season2(offset):
    now = datetime.now()

    other = now + relativedelta(months=offset * 3)
    season = get_season(other.month)
    other_month = season * 3
    _, month_day = calendar.monthrange(other.year, other_month)
    other += relativedelta(month=other_month, day=month_day)

    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)

    if now > other:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _season3(offset):
    now = datetime.now()
    other = now + relativedelta(months=offset * 3)
    season = get_season(other.month)

    start_month = (season - 1) * 3 + 1
    start = other + relativedelta(month=start_month, day=1)

    end_month = season * 3
    _, month_day = calendar.monthrange(other.year, end_month)
    end = other + relativedelta(month=end_month, day=month_day)

    start_date = yyyymmdd(start)
    end_date = yyyymmdd(end)

    return (start_date, end_date)


def _season4(offset):
    """之前三个季度，不包含当前的季度，之后N个季度包含当前的季度
    """
    now = datetime.now()
    if offset <= 0:
        other = now + relativedelta(months=-3)
        season = get_season(other.month)
        new_month = season * 3
        _, month_day = calendar.monthrange(other.year, new_month)
        end = other + relativedelta(month=new_month, day=month_day)

        other = now + relativedelta(months=3*offset)
        season = get_season(other.month)
        new_month = (season - 1) * 3 + 1
        start = other + relativedelta(month=new_month, day=1)

        start_date = yyyymmdd(start)
        end_date = yyyymmdd(end)
        return (start_date, end_date)
    else:
        other = datetime.now()
        season = get_season(other.month)
        new_month = (season - 1) * 3 + 1
        start = other + relativedelta(month=new_month, day=1)

        other = now + relativedelta(months=3*(offset-1))
        season = get_season(other.month)
        new_month = season * 3
        _, month_day = calendar.monthrange(other.year, new_month)
        end = other + relativedelta(month=new_month, day=month_day)

        start_date = yyyymmdd(start)
        end_date = yyyymmdd(end)
        return (start_date, end_date)


def _half_year(offset: int, compute_type: int):
    if compute_type == 0:
        return _half_year0(offset)
    return None


def _half_year0(offset):
    now = datetime.now()
    
    other = now + relativedelta(months=offset*6)
    
    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)
    
    if offset <= 0:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _half_year1(offset):
    pass


def _half_year2(offset):
    pass


def _half_year3(offset):
    pass


def _year(offset: int, compute_type: int):
    if compute_type == 0:
        return _year0(offset)
    elif compute_type == 1:
        return _year1(offset)
    elif compute_type == 2:
        return _year2(offset)
    elif compute_type == 3:
        return _year3(offset)
    return None


def _year0(offset):
    now = datetime.now()
    other = now + relativedelta(years=offset)
    
    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)
    
    if offset <= 0:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _year1(offset):
    now = datetime.now()
    other = now + relativedelta(years=offset, month=1, day=1)
    
    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)
    
    if now > other:
        return (other_date, now_date)
    else:
        return (now_date, other_date)
    


def _year2(offset):
    now = datetime.now()
    other = now + relativedelta(years=offset, month=12, day=31)
    
    now_date = yyyymmdd(now)
    other_date = yyyymmdd(other)
    
    if now > other:
        return (other_date, now_date)
    else:
        return (now_date, other_date)


def _year3(offset):
    now = datetime.now()
    
    start = now + relativedelta(years=offset, month=1, day=1)
    end = now + relativedelta(years=offset, month=12, day=31)
    
    start_date = yyyymmdd(start)
    end_date = yyyymmdd(end)
    return (start_date, end_date)
