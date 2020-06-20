# coding:utf-8
# Name:Hash.py
# Author:qi.yu
# Time:2020/6/20 19:27

"""
封装各种加密方法
"""

from hashlib import sha1
from hashlib import md5
import binascii

def my_md5(msg):
    """
    md5 算法加密
    :param msg:
    :return:
    """
    h1 = md5()
    h1.update(msg.encode('utf-8'))
    return h1.hexdigest()

def my_sha1(msg):
    """
    sha1 算法加密
    :param msg:
    :return:
    """
    sh = sha1()
    sh.update(msg.encode('utf-8'))
    return sh.hexdigest()

print(my_md5('213w1'))