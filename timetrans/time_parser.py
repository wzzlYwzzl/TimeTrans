import re

from timetrans.number import num_utils
from timetrans.timefunction import time_function


class TimeItem:
    """时间解析配置文件中的单个配置项
    """

    def __init__(self, pattern: str, value: str, time_type: str):
        """pattern、value、time_type对应配置文件的三列
        """
        self._pattern = pattern
        self._value = value
        self._time_type = time_type

    @property
    def pattern(self):
        return self._pattern

    @property
    def value(self):
        return self._value

    @property
    def time_type(self):
        return self._time_type


class TimeParser:

    def __init__(self, config_file: str):
        self._time_map = {}  # key: time_type, value: list[TimeItem]
        self.load_config(config_file)

    def load_config(self, config_file: str):
        """加载时间相关的配置
        """
        with open(config_file, mode='r+', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):  # 这一行是注释行
                    continue
                fields = line.split('\t')
                if len(fields) >= 3:
                    pattern = fields[0].strip()
                    value = fields[1].strip()
                    time_type = fields[2].strip()
                    patterns = pattern.split('$')
                    for pattern in patterns:
                        pattern = pattern.strip()
                        item = TimeItem(pattern, value, time_type)
                        self.add_time_item(item)
        self.sort_time_item()

    def add_time_item(self, time_item: TimeItem):
        """添加一个时间配置项
        """
        if time_item.time_type in self._time_map:
            item_list = self._time_map[time_item.time_type]
            item_list.append(time_item)
        else:
            item_list = []
            item_list.append(time_item)
            self._time_map[time_item.time_type] = item_list

    def sort_time_item(self):
        """对时间配置按照pattern的长度进行排序，这能尽量保证时间的解析
        是按照最长匹配进行的。
        """
        for key, value in self._time_map.items():
            self._time_map[key] = sorted(
                value, key=lambda item: len(item.pattern), reverse=True)

    def parse_time(self, time_str: str, time_type: str):
        """解析时间字符串，返回时间的标准表示。

        参数说明：
        time_str: 时间的文本表述，比如“今日”，“明天”，“2017年三季报”等等
        time_type: 要做怎样的解析，比如“day”表示按照单个日期解析；“period”表示
            按照区间日期解析；“report”按照报告期来解析。之所以有这个参数原因是：
            同一种表述，在不同的场景下有不同的解析。

        返回值：如果解析失败返回None
        """
        if time_type in self._time_map:
            item_list = self._time_map[time_type]
            for item in item_list:
                ret = self._handle_one_pattern(item, time_str)
                if ret:
                    return ret
            return None
        
        # 不限制time_type
        if time_type == 'all':
            for item_list in self._time_map.values():
                for item in item_list:
                    ret = self._handle_one_pattern(item, time_str)
                    if ret:
                        return ret
        else:
            return None

    def _handle_one_pattern(self, item: TimeItem, time_str: str):
        pattern = self._get_pattern(item.pattern)
        match_obj = re.search(pattern, time_str)
        if match_obj:
            match_str = match_obj.group()
            value_str = item.value
            if value_str.startswith('time2time'):
                return self.time2time(match_str)
            else:
                return self._get_time(match_str, value_str)
        else:
            return None

    def _get_pattern(self, pattern: str):
        """将配置文件中日期pattern中的N替换为数字识别正则表达式
        """
        base_pattern = pattern
        new_pattern = base_pattern.replace('N', num_utils.num_pattern)
        return new_pattern

    def _get_time(self, match_str: str, time_func: str):
        """根据匹配的时间字符串和对应的时间函数解析得到时间
        """
        time_func = self._replace_N_with_num(match_str, time_func)
        ret_time = time_function.exec_function(time_func)
        if ret_time:
            return ret_time
        else:
            return None

    def _replace_N_with_num(self, match_str: str, time_func: str):
        """把time_func中的N替换成match_str中的具体数字
        """
        pattern = re.compile(num_utils.num_pattern)
        index = 0
        while index < len(match_str) and 'N' in time_func:
            match = pattern.search(match_str[index:])
            if match:
                span = match.span()
                standard_num = num_utils.cn_num_translate(match.group())
                time_func = time_func.replace('N', str(standard_num), 1)
                index += span[1]
        return time_func

    def time2time(self, time_str: str):
        """这个时间函数解决如下时间表述：
        time (到|至|-) time的形式，要求time是如下一种形式：

        time的形式要求是day类型的日期表述
        """
        item_list = self._time_map['day']
        index = 0
        ret_list = []
        match_times = 0
        for item in item_list:
            if index < len(time_str) and match_times < 2:
                pattern = self._get_pattern(item.pattern)
            else:
                break

            while index < len(time_str) and match_times < 2:
                match_obj = re.search(pattern, time_str[index:])
                if match_obj:
                    match_str = match_obj.group()
                    value_str = item.value
                    ret = self._get_time(match_str, value_str)
                    if ret:
                        match_times += 1
                        ret_list.append(ret)
                    index += match_obj.span()[1]
                else:
                    break
        if len(ret_list) == 2:
            return tuple(ret_list)
        else:
            return None