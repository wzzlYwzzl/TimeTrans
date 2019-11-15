import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.day.n2time_day import n2time_day

test = 'n2time_day(2017)'
ret = n2time_day(test)
print(ret == '20171231')

test = 'n2time_day(201707)'
ret = n2time_day(test)
print(ret == '20170731')

test = 'n2time_day(20170823)'
ret = n2time_day(test)
print(ret == '20170823')

test = 'n2time_day(2017923)'
ret = n2time_day(test)
print(ret == '20170923')

test = 'n2time_day(2017123)'
ret = n2time_day(test)
print(ret == '20171203')