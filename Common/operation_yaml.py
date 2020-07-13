# coding:utf-8
# Name:operation_yaml.py
# Author:qi.yu
# Time:2020/6/21 10:54
"""
读取yaml数据
"""

import yaml
import os
import os.path
from Common import log
from ruamel import yaml

path_ya = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) + '/Testdata/Yaml/'

# def parse():
#     pages = {}
#     for root, dirs, files in os.walk(path_ya):
#         for name in files:
#             watch_file_path = os.path.join(root, name)
#             with open(watch_file_path, 'r') as f:
#                 page = yaml.safe_load(f)
#                 pages.update(page)
#         return pages
#
#
# class GetTestData:
#     @staticmethod
#     def get_value(key):
#         _page_list = {}
#         pages = parse()
#         return pages[key]





if __name__ == '__main__':
    # lists = GetTestData.get_value('login')
    # print(lists)
    aa = YamlHandle('login.yaml')
    # b = aa.get_yaml_value_of_key('login1.yaml','login')
    # print(type(b))
    abc = {
        'dsv1221d': {
            '888':'567'
        }
    }
    # b = aa.get_yaml_value_of_key()
    # print(b)
    aa.write_yaml_key_value('login','data',abc)



