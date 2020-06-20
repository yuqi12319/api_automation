# coding:utf-8
# Name:Shell.py
# Author:qi.yu
# Time:2020/6/21 0:56
"""
封装执行shell语句方法
"""

import subprocess

class Shell:
    @staticmethod
    def invoke(cmd):
        output,errors = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        o = output.decode('utf-8')
        return o
