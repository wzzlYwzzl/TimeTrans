import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.period.year_period import year_period

test = 'year_period(18,0,0)'
ret = year_period(test)
print(ret == ('20180101','20180630'))

test = 'year_period(18,1,0)'
ret = year_period(test)
print(ret == ('20180701','20181231'))

test = 'year_period(-1,0,1)'
ret = year_period(test)
print(ret == ('20180101','20180630'))

test = 'year_period(-1,1,1)'
ret = year_period(test)
print(ret == ('20180701','20181231'))

test = 'year_period(18,1,2)'
ret = year_period(test)
print(ret == ('20180101','20181231'))

test = 'year_period(-1,1,3)'
ret = year_period(test)
print(ret == ('20180101','20181231'))
