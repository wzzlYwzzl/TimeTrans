import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.day.year_month_day import year_month_day

"""注意下面的测试是和当前的日期相关的
"""

print("开始测试year_month_day")

test = 'year_month_day(29,11,30,0)'
ret = year_month_day(test)
print(ret == '20291130')

test = 'year_month_day(0,-1,-2,7)'
ret = year_month_day(test)
print(ret == '20191012')

test = 'year_month_day(2012,-1,-2,3)'
ret = year_month_day(test)
print(ret == '20121012')

test = 'year_month_day(-1,6,30,4)'
ret = year_month_day(test)
print(ret == '20180630')