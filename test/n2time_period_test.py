import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.period.n2time_period import n2time_period

test = 'n2time_period(2017)'
ret = n2time_period(test)
print(ret == ('20170101','20171231'))

test = 'n2time_period(201707)'
ret = n2time_period(test)
print(ret == ('20170701','20170731'))

test = 'n2time_period(20170823)'
ret = n2time_period(test)
print(ret == ('20170823','20170823'))

test = 'n2time_period(2017923)'
ret = n2time_period(test)
print(ret == ('20170923','20170923'))

test = 'n2time_period(2017123)'
ret = n2time_period(test)
print(ret == ('20171203','20171203'))