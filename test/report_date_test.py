import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.reportdate.report_date import report_date

test = 'report_date(2017,1,0)'
ret = report_date(test)
print(ret == '20170331')

test = 'report_date(-1,1,1)'
ret = report_date(test)
print(ret == '20180331')

test = 'report_date(0,1,2)'
ret = report_date(test)
print(ret == '20190331')

test = 'report_date(0,2,2)'
ret = report_date(test)
print(ret == '20190630')

test = 'report_date(0,3,2)'
ret = report_date(test)
print(ret == '20190930')

test = 'report_date(0,4,2)'
ret = report_date(test)
print(ret == '20181231')

test = 'report_date(0,0,2)'
ret = report_date(test)
print(ret == '20190930')