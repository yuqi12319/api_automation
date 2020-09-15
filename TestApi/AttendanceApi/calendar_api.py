# coding:utf-8
# Name:calendar_api.py
# Author:qi.yu
# Time:2020/9/14 6:14 下午
# Description:

from TestApi.consts_api import Const
import time, datetime


class CalendarApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def get_calendar_day_record(self, data):
        url = self.url_path + '/dukang-attendance/calendar/day/' + str(
            int(time.mktime(datetime.date.today().timetuple())) * 1000)
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res
