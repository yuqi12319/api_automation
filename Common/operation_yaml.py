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

path_ya = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) + '/TestData/Yaml/'


class YamlHandle:
    def __init__(self):
        self.log = log.MyLog()

    def read_yaml(self, file_name, mode='r'):
        try:
            with open(path_ya + file_name, mode, encoding='utf-8') as f:
                return list(yaml.safe_load_all(f))
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

    def read_yaml_return_list(self, file_name, mode='r'):
        with open(path_ya + file_name, mode, encoding='utf-8') as f:
            content = yaml.safe_load(f)
            data_list = []
            new_data_list = []
            for i in content:
                data_list.append(content[i])
            for j in data_list:
                a = []
                for k in j:
                    a.append(j[k])
                new_data_list.append(a)
            return new_data_list


if __name__ == '__main__':
    aa = YamlHandle()
    b = aa.read_yaml('ThirdParty/regist_company.yaml')
    print(b)
