# coding:utf-8
# Name:shift_api.py
# Author:qi.yu
# Time:2020/9/1 11:00 上午
# Description:

from TestApi.consts_api import Const


class ShiftApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 生成唯一id
    def get_id_generator(self):
        url = self.url_path + '/dukang-attendance/api/getIdGenerator'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res

    # 查询公司班次列表
    def get_company_shift(self, data):
        url = self.url_path + '/dukang-attendance/api/shift'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
