# Name:test_leave_form_apply.py
# Author:michelle.hou
# Time:2020-08-10 17:17

import allure
import pytest

from Common.operation_assert import Assertions
from Common.operation_yaml import YamlHandle
from TestApi.LeaveApi.LeaveApply import LeaveFormApply


@allure.feature('提交休假申请')
class TestLeaveFormApply:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @allure.title("按天休假")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('Leave/LeaveForm/leave_form_by_day_apply.yaml'))
    def test_leave_form_by_day_apply(self, data):
        print(data)
        # millis = int(round(time.time() * 1000))
        # print(millis)
        # 获取当前日期时间戳转换成ms
        # day_time = int(time.mktime(datetime.date.today().timetuple()))
        # print(int(round(day_time * 1000)))
        # stamp = int(round(day_time * 1000))
        # YamlHandle.write_yaml('Leave/LeaveForm/leave_form_by_day_apply.yaml', 'beginDate', stamp)

        res = LeaveFormApply(self.env).send_leave_form(data)
        print(res.json())
        Assertions().assert_in_text(res.json()['errmsg'], data['expect']['assert_result'])

    @allure.title("按班次休假")
    def test_leave_form_by_shift_apply(self, data):
        res = LeaveFormApply(self.env).send_leave_form(data)
        Assertions().assert_in_text(res.json()['errmsg'], data['expect']['assert_result'])

    @allure.title("按小时休假")
    def test_leave_form_by_hour_apply(self, data):
        res = LeaveFormApply(self.env).send_leave_form(data)
        Assertions().assert_in_text(res.json()['errmsg'], data['expect']['assert_result'])


if __name__ == '__main__':
    pytest.main(["-sv", "test_leave_form_apply.py", "--env", "test1"])
