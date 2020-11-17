# coding:utf-8
# Name:generate_employee_excel.py
# Author:qi.yu
# Time:2020/6/29 1:38 下午

from openpyxl import *
from Common.operation_random import *
import time
from random import choice
from faker import Faker


class Generate_Employee_excel:
    def __init__(self):
        self.wb = load_workbook('batch_employee.xlsx')
        self.temporaryworkers = load_workbook('batch_temporaryworker.xlsx')
        self.fake = Faker(locale='zh_CN')

    def add(self, count, job_number_start):
        '''
        :param count: 需要生成多少人
        :param job_number_start: 工号从几号开始
        :return:
        '''
        sheet = self.wb.active
        for i in range(2, count + 2):
            a = 'A' + str(i)
            sheet[a] = i - 2 + job_number_start  # 工号
            name = self.fake.name()
            b = 'B' + str(i)
            sheet[b] = name  # 显示名字
            c = 'C' + str(i)
            sheet[c] = name  # 真实姓名
            d = 'D' + str(i)
            sheet[d] = self.fake.phone_number()  # 手机号码
            sex = ['男', '女', '其他']
            e = 'E' + str(i)
            sheet[e] = choice(sex)  # 性别
            f = 'F' + str(i)
            sheet[f] = '居民身份证'  # 证件类型
            idcard = self.fake.ssn()
            g = 'G' + str(i)
            sheet[g] = idcard  # 身份证号码
            h = 'H' + str(i)
            sheet[h] = date_of_birth_by_idcard(idcard)  # 出生日期
            k = 'K' + str(i)
            sheet[k] = '全职'  # 雇佣类型

        self.wb.save(str(int(time.time())) + '.xlsx')

    def generate_temporary_workers_excel(self, count):
        """
        :param count: 需要生成多少人
        """
        sheet = self.temporaryworkers.get_sheet_by_name('导入数据')
        for item in range(2, count + 2):
            idcard = self.fake.ssn()
            a = 'A' + str(item)
            sheet[a] = idcard   # 身份证号码
            b = 'B' + str(item)
            sheet[b] = self.fake.name()     # 姓名
            sex = ['男', '女', '其他']
            c = 'C' + str(item)
            sheet[c] = choice(sex)      # 性别
            d = 'D' + str(item)
            sheet[d] = '汉族'     # 民族
            e = 'E' + str(item)
            sheet[e] = date_of_birth_by_idcard(idcard)  # 出生日期
            h = 'H' + str(item)
            sheet[h] = self.fake.address()      # 当前住址
            i = 'I' + str(item)
            sheet[i] = self.fake.phone_number()     # 联系电话
            j = 'J' + str(item)
            sheet[j] = self.fake.name()     # 紧急联络人姓名
            k = 'K' + str(item)
            sheet[k] = self.fake.phone_number()     # 紧急联络人电话

        self.temporaryworkers.save(str(int(time.time())) + '.xlsx')


if __name__ == '__main__':
    obj = Generate_Employee_excel()
    obj.add(100, 1)
    # obj.generate_temporary_workers_excel(1000)