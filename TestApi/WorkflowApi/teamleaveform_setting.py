# Name:teamleaveform_setting.py
# Author:michelle.hou
# Time:2020-08-05 15:50

from TestApi.consts_api import Const


class TeamLeaveApprovalSetting(Const):
    # 创建团队休假审批流
    def creat_team_leave_approval(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response

    #  获取团队休假审批流列表
    def get_team_leave_approval(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('get', url, params=data['params'], headers=self.headers)
        return response
    # 删除团队休假审批流

    def delete_team_leave_approval(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('DELETE', url,  params=data['params'], headers=self.headers)
        return response
