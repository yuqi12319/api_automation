# coding:utf-8
# Name:workflow_set_api.py
# Author:qi.yu
# Time:2020/9/15 5:25 下午
# Description:

from TestApi.consts_api import Const


class WorkflowSetApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 加班，补卡，外出，离职审批流列表接口
    def attendance_approval_list_api(self, data):
        url = self.url_path + '/dukang-attendance/api/workflow_settings?type='
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 更新审批流设置信息
    def update_attendance_approval(self, data):
        url = self.url_path + '/dukang-attendance/api/workflow_settings/' + str(data['workflow_setting_id'])
        res = self.request.send_request_method('put', url=url , json=data['body'], headers=self.headers)
        return res
