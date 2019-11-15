"""和时间函数的参数解析有关的工具函数
"""


def get_params(func_str: str):
    """从时间函数获取函数的参数。
    约定函数都是如下形式：function_name(param1,param2,param3,...)
    返回的是按照先后顺序的参数list[str]。

    如果func_str是空或者是None，则返回空的list。
    """
    if func_str:
        try:
            start_pos = func_str.index('(')
            end_pos = func_str.index(')')
        except Exception:
            return []

        params_str = func_str[start_pos+1:end_pos]
        params = params_str.split(',')
        return params
    else:
        return []
