# coding:utf-8
# Name:leave_setting_api.py
# Author:qi.yu
# Time:2020/8/25 4:38 下午
# Description:休假组设置

from TestApi.consts_api import Const


class LeaveSettingApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_leave_group_api(self, data):
        url = self.url_path + '/leave/leave_groups_for_web'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 新增休假组（法定年假，福利年假，法定病假，福利病假等）接口
    def add_leave_groups_api(self, data):
        url = self.url_path + '/leave/leave_groups/all'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 删除休假组
    def delete_leave_group(self, data):
        url = self.url_path + '/leave/leave_groups/' + str(data['leaveGroupId'])
        res = self.request.send_request_method('delete', url=url, headers=self.headers)
        return res