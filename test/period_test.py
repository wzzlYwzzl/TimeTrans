import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.period.period import period

"""
print("测试day")

test = 'period(-7,0,0)'
ret = period(test)
print(ret == ('20191107','20191114'))


test = 'period(-7,0,1)'
ret = period(test)
print(ret == ('20191105','20191114'))

test = 'period(7,0,0)'
ret = period(test)
print(ret == ('20191114','20191121'))

test = 'period(7,0,1)'
ret = period(test)
print(ret == ('20191114','20191125'))
"""

"""
print("测试week")

test = 'period(-1,1,0)'
ret = period(test)
print(ret == ('20191107','20191114'))

test = 'period(1,1,0)'
ret = period(test)
print(ret == ('20191114','20191121'))

test = 'period(-1,1,1)'
ret = period(test)
print(ret == ('20191104','20191114'))

test = 'period(-1,1,2)'
ret = period(test)
print(ret == ('20191110','20191114'))

test = 'period(1,1,2)'
ret = period(test)
print(ret == ('20191114','20191124'))

test = 'period(-1,1,3)'
ret = period(test)
print(ret == ('20191104','20191110'))

test = 'period(1,1,3)'
ret = period(test)
print(ret == ('20191118','20191124'))

test = 'period(0,1,3)'
ret = period(test)
print(ret == ('20191111','20191117'))

"""

"""

print('测试month')

test = 'period(0,2,3)'
ret = period(test)
print(ret == ('20191101','20191130'))

test = 'period(-1,2,3)'
ret = period(test)
print(ret == ('20191001','20191031'))

test = 'period(-1,2,0)'
ret = period(test)
print(ret == ('20191014','20191114'))

test = 'period(-1,2,1)'
ret = period(test)
print(ret == ('20191001','20191114'))

test = 'period(-1,2,2)'
ret = period(test)
print(ret == ('20191031','20191114'))

test = 'period(1,2,2)'
ret = period(test)
print(ret == ('20191114','20191231'))

"""

"""

print("测试season")

test = 'period(1,3,0)'
ret = period(test)
print(ret == ('20191115','20200215'))

test = 'period(-1,3,1)'
ret = period(test)
print(ret == ('20190701','20191115'))

test = 'period(1,3,2)'
ret = period(test)
print(ret == ('20191115','20200331'))

test = 'period(0,3,3)'
ret = period(test)
print(ret == ('20191001','20191231'))

test = 'period(-3,3,4)'
ret = period(test)
print(ret == ('20190101','20190930'))

test = 'period(3,3,4)'
ret = period(test)
print(ret == ('20191001','20200630'))

"""

"""

print("测试half_year")

test = 'period(-1,4,0)'
ret = period(test)
print(ret == ('20190515','20191115'))

"""

print("测试year")

test = 'period(-1,5,0)'
ret = period(test)
print(ret == ('20181115','20191115'))

test = 'period(-1,5,1)'
ret = period(test)
print(ret == ('20180101','20191115'))

test = 'period(1,5,2)'
ret = period(test)
print(ret == ('20191115','20201231'))

test = 'period(-1,5,3)'
ret = period(test)
print(ret == ('20180101','20181231'))

test = 'period(0,5,3)'
ret = period(test)
print(ret == ('20190101','20191231'))

test = 'period(1,5,3)'
ret = period(test)
print(ret == ('20200101','20201231'))