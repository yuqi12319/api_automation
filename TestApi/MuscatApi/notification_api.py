# coding:utf-8
# Name:notification_api.py
# Author:qi.yu
# Time:2020/9/17 4:16 下午
# Description:

from TestApi.consts_api import Const

class NotificationApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_notifications_list_api(self, data):
        url = self.url_path + '/muscat/notifications/list'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res