class Number:
    def __init__(self, offset, length, value):
        self.offset = offset
        self.length = length
        self.value = value


# 初始化一些基本参数，包括中文基本数字0-9与单位
chinese_num = {'零': 0, '一': 1, '壹':1, '二': 2, '贰': 2, '两': 2, '三': 3,
               '叁': 3, '四': 4, '肆': 4, '五': 5, '伍': 5, '六': 6, '陆': 6, 
               '七': 7, '柒': 7, '八': 8, '捌': 8, '九': 9, '玖': 9}

rules = {'亿': 100000000, '万': 10000, '千': 1000, '仟': 1000, '百': 100, 
         '佰': 100, '十': 10, '拾': 10, '个': 1}

float_point = set(['.','点'])

# 日期识别中，这个正则表达式用于检测其中的N
num_pattern = '[0123456789零一二三四五六七八九十百千万亿]+'


def preprocess_data(num):
    """
    预处理数据，包括清除数据中的','和'个'
    :param num: 中文数字（包括混合形式）
    :return: 返回处理后的数字
    """
    new_num = num
    for idx in reversed(range(len(num))):
        if num[idx] == '个' or num[idx] == ',':
            new_num = new_num[:idx] + new_num[idx + 1:]

    return new_num


def find_size(num):
    """
    依据单位从大到小原则，找出这个中文数字（包括混合形式）的最大单位
    :param num: 中文数字（包括混合形式）
    :return: 返回一个tuple，其中第一个元素是最大单位，第二个元素是这个单位所代表的大小
    """
    num_type = '个'
    for key in rules:
        if key in num:
            return key, rules[key]

    return num_type, rules[num_type]


def test_for_non_unit_num(num):
    """
    此方法将会对无单位中文数字进行检测，如果符合条件直接输出结果
    :param num: 中文数字（包括各种形式）
    :return: 如果不符合条件，返回0，如果符合则返回对应的值
    """
    en_num = 0
    base = 1
    for idx in reversed(range(len(num))):
        # 如果此下标对应的字是单位则返回0
        if num[idx] in rules or num[idx:idx + 2] in rules or num[idx] in float_point:
            return 0
        if num[idx].isdigit():
            en_num = en_num + int(num[idx]) * base
        else:
            en_num = en_num + chinese_num[num[idx]] * base

        base = base * 10

    return en_num


def test_multiple_nums(num):
    """
    检测是否此数字需要分割成多个数字
    :param num: 中文数字（包括各种形式）
    :return: 返回一个数组，里面存储切割后的数字
    """
    if len(num) <= 2 or num.isdigit():
        return [num]

    # 获取这个数字的最大单位以及这个单位的下标值
    unit_inf = find_size(num)
    unit_idx = num.find(unit_inf[0])
    if unit_inf[0] == '万' or unit_inf[0] == '亿':
        # 首先获取之后部分切割后的中文数字数组
        nums_after = test_multiple_nums(num[unit_idx + 1:])
        # 如果是1则前面部分不需要切割
        if unit_idx == 1:
            return [num[:2]+nums_after[0]]+nums_after[1:]
        # 如果此单位之前一位是数字则切割
        if num[unit_idx - 1] in chinese_num:
            if num[unit_idx - 2] != '十':
                return [num[:unit_idx - 1]] + [num[unit_idx - 1:unit_idx + 1] + nums_after[0]] + nums_after[1:]
            else:
                return [num[:unit_idx + 1] + nums_after[0]] + nums_after[1:]
        # 如果此单位前一位是单位则检测前面部分
        if num[unit_idx-1] in rules:
            nums_before = test_multiple_nums(num[:unit_idx])
            return nums_before[:-1] + [nums_before[-1] + unit_inf[0] + nums_after[0]] + nums_after[1:]

    if unit_inf[0] == '千':
        # 首先获取单位之后部分切割后的中文数字数组
        nums_after = test_multiple_nums(num[unit_idx + 1:])
        # 如果是1则不需要检测
        if unit_idx == 1:
            return [num[:2] + nums_after[0]] + nums_after[1:]
        else:
            # 不是则切割
            return [num[:unit_idx - 1]] + [num[unit_idx - 1:unit_idx + 1] + nums_after[0]] + nums_after[1:]

    if unit_inf[0] == '百':
        # 如果是1，直接返回
        if unit_idx == 1:
            return [num]
        else:
            # 不是则切割
            return [num[:unit_idx - 1]] + [num[unit_idx - 1:]]

    return [num]


def get_value(num):
    """
    获取经过处理的中文数字（包括混合形式）代表的阿拉伯形式值
    :param num: 中文数字（包括混合形式）
    :return: 返回num的阿拉伯数字形式
    """
    # 如果长度为0则返回0值
    if len(num) == 0:
        return 0

    # 如果这个数字是一个阿拉伯数字则转化成int返回
    if num.isdigit():
        return int(num)

    # 对个位数以及单个’十‘和首个字是’十‘的形式进行单独处理
    size = find_size(num)
    if size[0] == '个':
        if len(num) > 1:  # 处理小数数字，或者是连续的大写数字。一点一三，1.13
            ch_list = [str(chinese_num[tet])
                       if tet in chinese_num else tet for tet in num]
            new_num = ''.join(ch_list)
            if is_float(new_num):
                new_num = new_num.replace('点','.')
                return float(new_num)
            else:
                return int(new_num)

        if num[0] in chinese_num:
            return chinese_num[num[0]]
        else:
            return int(num[0])
    elif num == '十':
        return 10
    else:
        if num[0] == '十':
            num = '一' + num
        if num[0:2] == '零十':
            num = '一' + num[1:]
        nums = num.split(size[0])

        if len(nums[1]) == 1:
            return get_value(nums[0]) * size[1] + get_value(nums[1]) * int(size[1] / 10)
        else:
            return get_value(nums[0]) * size[1] + get_value(nums[1])


def cn_num_translate(num):
    """
    计算中文数字（包括混合形式）的值
    :param num:
    :return:

    注意：这里不支持浮点数
    """
    negative = 1
    if num[0] == '-' or num[0] == '负':
        negative = -1
        num = num[1:]
    elif num[0] == '+' or num[0] == '正':
        num = num[1:]

    value = test_for_non_unit_num(num)
    if value > 0:
        return value

    # 首先用“零”对句子进行切割
    #nums = num.split('零')
    #for sub_num in nums:
    #    value = value + get_value(sub_num)
    value = get_value(num)
    return value * negative


def is_float(num: str):
    """判断num字符串是否是小数。判断方法就是
    是否包含“.”和“点”。
    """
    if '.' in num or '点' in num:
        return True
    return False


def process_sentence(line):
    """
    处理句子，把其中的中文数字，包括各种形式，提取出来
    :param line: 一句话
    :return: 返回这句话中中文数字的数组
    """
    nums_inf = []
    num = ''
    i = 0
    while i < len(line):
        # 如果i小于句子长度并且当前的字是单位或者数字或者逗号便进入循环
        while i < len(line) and \
                ((line[i].isdigit() or line[i] in chinese_num or line[i] in rules) or line[i] == ','):
            num = num + line[i]
            i = i + 1

        # 如果num大于零，则表示检测到了中文数字（各种类型）
        if len(num) != 0:
            process_num = preprocess_data(num)
            # 检测“三十三百”这种情况
            nums = test_multiple_nums(process_num)
            nums_inf = nums_inf + \
                [(sub_num, i - (len(num) - process_num.find(sub_num)) + 1)
                 for sub_num in nums]
            num = ''
            # nums_inf.append((preprocess_data(num), i - len(num) + 1))

        i = i + 1

    return nums_inf


def sentence_num_translate(sentence):
    """
    计算一个句子中数字信息的数组
    :param sentence: 一个句子
    :return: 返回这个句子中数字信息的数组
    """
    nums_inf = process_sentence(sentence)
    nums_set = []
    for num_inf in nums_inf:
        value = cn_num_translate(num_inf[0])
        nums_set.append(Number(num_inf[1], len(num_inf[0]), value))

    return nums_set
