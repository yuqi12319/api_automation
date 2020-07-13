# coding:utf-8
# Name:operation_yaml.py
# Author:qi.yu
# Time:2020/6/21 10:54
"""
读取yaml数据
"""

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

class YamlHandle:
    def __init__(self):
        self.log = log.MyLog()

    def read_yaml(self, file_name, mode='r'):
        try:
            with open(path_ya + file_name, mode, encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.log.error(f'{file_name} yaml read error,error as {e}')
            return False

    def write_yaml(self, file_name, major_key, key, value):
        try:
            with open(path_ya + file_name, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                content[major_key][key] = value
                # print(type(content))
            with open(path_ya + file_name, 'w', encoding='utf-8') as ff:
                yaml.dump(content, ff, Dumper=yaml.RoundTripDumper)
            return True
        except Exception as e:
            self.log.error(f'{file_name} yaml write error,error as {e}')
            return False


if __name__ == '__main__':
    aa = YamlHandle()
    b = aa.read_yaml('login.yaml')
