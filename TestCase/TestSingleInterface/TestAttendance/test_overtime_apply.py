import pytest
from Common.operation_assert import *
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.AttendanceApi.overtime_api import OvertimeApi


class TestOvertime:

    @pytest.fixture(autouse=True)
    def env_prepare(self, env):
        self.env = env

    @pytest.mark.parametrize("data", YamlHandle().read_yaml('SingleInterfaceData/Attendance/overtime.yaml'))
    def test_apply_overtime(self, data):
        print(data)
        res = OvertimeApi(self.env).send_overtime_apply_api(data)
        # print(res.status_code())
        print(type(res))
        status_code = res.status_code
        if status_code == 200:

            Assertions().assert_text(res.json()['errmsg'], data['expect']['assert_result'])
        else:
            print("请求未成功请检查，status_code= %s" % status_code)

    @pytest.mark.parametrize("data", YamlHandle().read_yaml('SingleInterfaceData/Attendance/Team_OverTime_Apply.yaml'))
    def test_team_overtime_apply(self, data):
        print(data)
        res = OvertimeApi(self.env).send_overtime_apply_api(data)
        # print(res.status_code())
        print(type(res))
        print(res.json())
        # print(res.status_code)
        status_code = res.status_code
        if status_code == 200:
            Assertions().assert_text(res.json()['data'], data['expect']['assert_data'])
        else:
            print("请求未成功请检查，status_code= %s" % status_code)

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(['-s', 'test_overtime_apply.py', '--env', 'test1'])
