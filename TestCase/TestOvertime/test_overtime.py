import pytest
from Common.operation_assert import *
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from TestApi.OvertimeApi.Overtimeapply import OvertimeApply


class TestOvertime:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test1')

    @pytest.mark.parametrize("data", YamlHandle().read_yaml('OvertimeApply/overtime.yaml'))
    def test_apply_overtime(self, data):
        print(data)
        res = OvertimeApply().send_apply_api(self.url_path, data)
        # print(res.status_code())
        print(type(res))
        status_code = res.status_code
        if status_code == 200:

            Assertions().assert_text(res.json()['errmsg'], data['expect']['assert_result'])
        else:
            print("请求未成功请检查，status_code= %s" % status_code)

    @pytest.mark.parametrize("data", YamlHandle().read_yaml('OvertimeApply/Team_OverTime_Apply.yaml'))
    def test_team_overtime_apply(self, data):
        print(data)
        res = OvertimeApply().send_apply_api(self.url_path, data)
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
    pytest.main(['-s', 'test_overtime.py'])
