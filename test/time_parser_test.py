import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.time_parser import TimeParser

config_file = '/Users/caoxiaojie/pythonCode/TimeTrans/time.txt'

time_parser = TimeParser(config_file)

ret = time_parser.parse_time('今天','day')
print(ret == '20191118')

ret = time_parser.parse_time('今年','period')
print(ret == ('20190101','20191118'))