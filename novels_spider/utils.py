#!/usr/bin/env python3
# encoding: utf-8
'''
@author: JackyLove
@contact: asaltedfishz@gmail.com
@file: utils.py
@time: 2019-06-17 20:31
'''
import time
from functools import wraps


def fn_timer(function):
    '''
    函数计时装饰器
    :param function: 函数对象
    :return: 装饰器
    '''

    @wraps(function)
    def function_timer(*args, **kwargs):
        # 开始时间
        t0 = time.time()
        # 调用函数
        result = function(*args, **kwargs)
        # 结束时间
        t1 = time.time()
        # 打印函数耗时
        print('[finished function:{func_name} in {time:.2f}s]'.format(func_name=function.__name__, time=t1 - t0))
        return result

    return function_timer


# 测试
@fn_timer
def add(x, y):
    time.sleep(1)
    return x + y


if __name__ == '__main__':
    # 测试
    add(1, 2)
