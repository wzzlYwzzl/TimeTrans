import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.period.season_period import season_period

test = 'season_period(2018,1,0)'
ret = season_period(test)
print(ret == ('20180101','20180331'))

test = 'season_period(18,2,0)'
ret = season_period(test)
print(ret == ('20180401','20180630'))

test = 'season_period(2018,3,0)'
ret = season_period(test)
print(ret == ('20180701','20180930'))

test = 'season_period(18,4,0)'
ret = season_period(test)
print(ret == ('20181001','20181231'))

test = 'season_period(-1,1,1)'
ret = season_period(test)
print(ret == ('20180101','20180331'))

test = 'season_period(-1,2,1)'
ret = season_period(test)
print(ret == ('20180401','20180630'))

test = 'season_period(-1,3,1)'
ret = season_period(test)
print(ret == ('20180701','20180930'))

test = 'season_period(-1,4,1)'
ret = season_period(test)
print(ret == ('20181001','20181231'))