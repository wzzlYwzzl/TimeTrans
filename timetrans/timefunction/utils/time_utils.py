def parse_year(year: str):
    """分析年份的字符串，得到有效的年份。

    如下约定：
    1. 要求字符串year的长度是2或者4；

    2. 如果year是四位整数，比如1988，2001之类，那么年份就是year对应的数字；
    3. 如果year是大于0，小于50，比如19，18，08等，则表示2000年之后的年份，2019，2018，2008；
    4. 如果year大于等于50，小于100，比如98，78，则表示1998、1978。

    如果不合法，则返回0
    """
    if year and (len(year) == 4 or len(year) == 2):
        year_int = int(year)
        if year_int > 1000 and year_int < 2100:
            return year_int
        elif year_int > 0 and year_int < 50:
            return 2000 + year_int
        elif year_int >= 50 and year_int < 100:
            return 1900 + year_int
        else:
            return 0
    else:
        return 0


def get_season(month: int):
    """根据month，输出其所在的季度。
    1~3月属于1季度；
    4~6月属于2季度；
    7~9月属于3季度；
    10~12月属于4季度；
    """
    a = int(month / 3)
    b = month % 3
    
    if b:
        return a + 1
    else:
        return a