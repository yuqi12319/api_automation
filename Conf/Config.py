# coding:utf-8
# Name:Config.py
# Author:qi.yu
# Time:2020/6/24 5:31 下午

from configparser import ConfigParser
from Common import Log
import os

class Config:

    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir)))

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.log = Log.MyLog()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini')
        self.xml_report_path = Config.path_dir+'/Report/xml'
        self.html_report_path = Config.path_dir+'/Report/html'

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确认配置文件存在！")

        self.config.read(self.conf_path,encoding='utf-8')

    def get_conf(self,title,value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title,value)

    def set_conf(self,title,value,text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title,value,text)
        with open(self.conf_path,"w+") as f:
            return self.config.write(f)

    def add_conf(self,title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path,"w+") as f:
            return self.config.write(f)



if __name__ == '__main__':
     ab = Config()
     text = ab.get_conf('private_test1','tester')
     print(text)
