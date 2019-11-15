import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.timefunction.day.week import week

print("开始测试week")

test = 'week(0,0,0)' # 对应于“今天”
ret = week(test)
print(ret == '20191114')

test = 'week(-1,0,0)' # 对应于上周
ret = week(test)
print(ret == '20191107')

test = 'week(-1,0,1)' # 对应于上周一
ret = week(test)
print(ret == '20191104')

test = 'week(0,2,1)' # 对应于本周三
ret = week(test)
print(ret == '20191113')

test = 'week(0,4,1)' # 对应于本周五
ret = week(test)
print(ret == '20191115')

test = 'week(2,1,1)' # 下下周二
ret = week(test)
print(ret == '20191126')