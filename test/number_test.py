import sys

sys.path.append('/Users/caoxiaojie/pythonCode/TimeTrans')

from timetrans.number.num_utils import cn_num_translate

ret = cn_num_translate('三十')
print(ret)

ret = cn_num_translate('22')
print(ret)