import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.period.month_period import month_period

test = 'month_period(2018,1,0,0)'
ret = month_period(test)
print(ret == ('20180101','20180131'))

test = 'month_period(18,5,0,0)'
ret = month_period(test)
print(ret == ('20180501','20180531'))

test = 'month_period(-1,1,1,0)'
ret = month_period(test)
print(ret == ('20180101','20180131'))

test = 'month_period(2018,1,0,1)'
ret = month_period(test)
print(ret == ('20180101','20180115'))

test = 'month_period(2018,1,0,2)'
ret = month_period(test)
print(ret == ('20180115','20180131'))