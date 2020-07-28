# coding:utf-8
# Name:generate_employee_excel.py
# Author:qi.yu
# Time:2020/6/29 1:38 下午

from openpyxl import *
from Common.operation_random import *
import time


class Generate_Employee_excel:
    def __init__(self):
        self.wb = load_workbook('batch_employee.xlsx')

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
            name = random_name()
            b = 'B' + str(i)
            sheet[b] = name[0]  # 显示名字
            c = 'C' + str(i)
            sheet[c] = name[0]  # 真实姓名
            d = 'D' + str(i)
            sheet[d] = random_phone()  # 手机号码
            e = 'E' + str(i)
            sheet[e] = name[1]  # 性别
            f = 'F' + str(i)
            sheet[f] = '居民身份证'  # 证件类型
            idcard = random_idcard()
            g = 'G' + str(i)
            sheet[g] = idcard  # 身份证号码
            h = 'H' + str(i)
            sheet[h] = date_of_birth_by_idcard(idcard)  # 出生日期
            k = 'K' + str(i)
            sheet[k] = '全职'  # 雇佣类型

        self.wb.save(str(int(time.time())) + '.xlsx')


if __name__ == '__main__':
    obj = Generate_Employee_excel()
    obj.add(20, 101)
