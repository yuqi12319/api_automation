import pytest
from Common.operation_assert import *
from Common.operation_yaml import YamlHandle
from Conf.config import Config
from Robot.Overtime.api_first_Team import OvertimeApply


class TestOvertime:

    def setup_class(self):
        self.url_path = Config().get_conf('test_env', 'test1')

    @pytest.mark.parametrize("data", YamlHandle().read_yaml('OvertimeApply/overtime.yaml'))
    def test_apply_overtime(self, data):
        print(data)
        res = OvertimeApply().send_apply_api(self.url_path, data)
        # print(res.status_code())
        print(type(res))
        Assertions().assert_text(res.json()['errmsg'], data['expect']['assert_result'])
        # Assertions().assert_text(res.json()['errcode'], data['expect']['assert_type'])

    @pytest.mark.skip
    @pytest.mark.parametrize("data", YamlHandle().read_yaml('OvertimeApply/Team_OverTime_Apply.yaml'))
    def test_team_overtime_apply(self, data):
        print(data)
        res = OvertimeApply().send_apply_api(self.url_path, data)
        # print(res.status_code())
        print(type(res))
        Assertions().assert_text(res.json()['data'], data['expect']['assert_data'])

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main(['-s', 'test_overtime.py'])
