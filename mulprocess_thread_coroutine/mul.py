#!/usr/bin/env python3
# encoding: utf-8
'''
@author: JackyLove
@contact: asaltedfishz@gmail.com
@file: mul.py
@time: 2019-06-17 15:58
'''
import time
from functools import wraps
import threading
from concurrent.futures import ThreadPoolExecutor

def fn_timer(function):
    '''
    函数计时装饰器
    :param function: 函数对象
    :return: 装饰器
    '''
    @wraps(function)
    def function_timer(*args,**kwargs):
        #开始时间
        t0 = time.time()
        #调用函数
        result = function(*args,**kwargs)
        #结束时间
        t1 = time.time()
        #打印函数耗时
        print('[finished function:{func_name} in {time:.2f}s]'.format(func_name = function.__name__,time=t1-t0))
        return result
    return function_timer

#测试
@fn_timer
def add(x,y):
    time.sleep(1)
    return x+y

#20个网页
urls = ['https://baike.baidu.com/item/%E8%87%AA%E7%94%B1%E8%BD%AF%E4%BB%B6',
        'https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%E8%AF%AD%E8%A8%80',
        'https://baike.baidu.com/item/%E5%9F%BA%E9%87%91%E4%BC%9A',
        'https://baike.baidu.com/item/%E5%88%9B%E6%96%B02.0',
        'https://baike.baidu.com/item/%E5%95%86%E4%B8%9A%E8%BD%AF%E4%BB%B6',
        'https://baike.baidu.com/item/%E5%BC%80%E6%94%BE%E6%BA%90%E4%BB%A3%E7%A0%81',
        'https://baike.baidu.com/item/OpenBSD',
        'https://baike.baidu.com/item/%E8%A7%A3%E9%87%8A%E5%99%A8',
        'https://baike.baidu.com/item/%E7%A8%8B%E5%BA%8F/71525',
        'https://baike.baidu.com/item/%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80',
        'https://baike.baidu.com/item/C%2B%2B',
        'https://baike.baidu.com/item/%E8%B7%A8%E5%B9%B3%E5%8F%B0',
        'https://baike.baidu.com/item/Web/150564',
        'https://baike.baidu.com/item/%E7%88%B1%E5%A5%BD%E8%80%85',
        'https://baike.baidu.com/item/%E6%95%99%E5%AD%A6',
        'https://baike.baidu.com/item/Unix%20shell',
        'https://baike.baidu.com/item/TIOBE',
        'https://baike.baidu.com/item/%E8%AF%BE%E7%A8%8B',
        'https://baike.baidu.com/item/MATLAB',
        'https://baike.baidu.com/item/Perl']

#耗时任务：听音乐
def music(name):
    print('I am listening to music {0}'.format(name))
    time.sleep(1)

#耗时任务:看电影
def movie(name):
    print('I am watching movie {0}'.format(name))
    time.sleep(5)


#单线程操作
@fn_timer
def single_thread():
    for i  in range(10):
        music(i)
    for i in range(2):
        movie(i)

#多线程执行:听10首音乐，看2部电影
@fn_timer
def multi_thread():
    #线程列表
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=music,args=(i,)))
    for i in range(2):
        threads.append(threading.Thread(target=movie,args=(i,)))

    for t in threads:
        #设为守护线程
        t.setDaemon(True)
        #开始线程
        t.start()
    for t in threads:
        t.join()


#线程池执行：听10首歌，看2部电影
@fn_timer
def use_pool():
    pool = ThreadPoolExecutor(max_workers=20)
    pool.map(music,range(10))
    pool.map(movie, range(2))
    pool.shutdown()
if __name__ == '__main__':
    #测试
    #single_thread()
    multi_thread()
    # use_pool()