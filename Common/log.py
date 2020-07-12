# coding:utf-8
# Name:log.py
# Author:qi.yu
# Time:2020/6/20 13:34

"""
封装log方法
"""

import logging
import os
import time

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger()
level = 'default'

def creat_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename,mode='w',encoding='utf-8')
        fd.close()
    else:
        pass

def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)

def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)

def get_current_time():
    return time.strftime(MyLog.date,time.localtime(time.time()))

class MyLog:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = path+'/Log/log.log'
    err_file = path+'/Log/error.log'
    logger.setLevel(LEVELS.get(level,logging.NOTSET))
    creat_file(log_file)
    creat_file(err_file)
    date = '%Y-%m-%d %H:%M:%S'

    handler = logging.FileHandler(log_file,encoding='utf-8')
    err_handler = logging.FileHandler(err_file,encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logging.debug("[DEBUG    " + get_current_time() + "]" + log_meg)
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logging.debug("[INFO     " + get_current_time() + "]" + log_meg)
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logging.debug("[WARNING  " + get_current_time() + "]" + log_meg)
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logging.debug("[ERROR    " + get_current_time() + "]" + log_meg)
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logging.debug("[CRITICAL " + get_current_time() + "]" + log_meg)
        remove_handler('critical')

if __name__ == '__main__':
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error")
    MyLog.critical("This is critical message")