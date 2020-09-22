# Name:test_employee_unactive.py
# Author:lin
# Time:2020/8/25 10:00 上午


import pytest
import allure
import time

from Common.log import MyLog
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.EmployeeApi.workforce_employee_domain import WorkforceEmployeeDomain
from TestApi.MuscatApi.muscat import Muscat
from TestApi.UserApi.third_sys_user_api import ThirdSysUserApi
from Common.operation_mysql import *
import Common.consts


class TestEmployeeActive:

    @pytest.fixture(scope='class')
    def setup_class(self, env):
        company_id = str()
        employee_id = str()
        if Common.consts.COMPANY_INFORMATION:
            company_id = Common.consts.COMPANY_INFORMATION[0]['company_id']
            employee_id = Common.consts.COMPANY_INFORMATION[0]['employee_id']
        else:
            my_companies_res = Muscat(env).get_my_companies_api()
            if my_companies_res.json()['data']:
                company_id = my_companies_res.json()['data'][0]['company_id']
                brief_profile_data = YamlHandle().read_yaml('SingleInterfaceData/Employee/brief_profile.yaml')[0]
                brief_profile_data['params']['company_id'] = company_id
                brief_profile_res = EmployeeApi(env).brief_profile_api(brief_profile_data)
                employee_id = brief_profile_res.json()['data']['employee_id']
            else:
                MyLog().error('当前用户下没有公司列表')
        return env, company_id, employee_id

    @pytest.mark.smoke
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/EmployeeManagerActivateScene/main_scene.yaml'))
    def test_main_sence(self, data, setup_class):
        # with allure.step('第一步，获取未激活员工'):

        # 获取员工未激活集合
        data['unactive']['headers']['x-dk-token'] = Common.consts.ACCESS_TOKEN[0]
        data['unactive']['params']['companyId'] = setup_class[1]
        employee_unactive_res = WorkforceEmployeeDomain(setup_class[0]).employee_unactice(data['unactive'])
        Assertions().assert_mode(employee_unactive_res, data['unactive'])

        # with allure.step('第二步，获取激活员工链接'):
        #     # 获取激活链接（暂不可用）
        #     t = time.time()
        #     data['active_url']['params']['timestamp'] = int(round(t * 1000))
        #     active_url_res = WorkforceEmployeeDomain(self.env).active_QRcode(data['active_url'])
        #     Assertions().assert_mode(active_url_res, data['active_url'])
        # 拿到未激活员工手机号

        mobile = list()
        # mobile.append(15383709615)
        if employee_unactive_res.json()['data']:
            for i in range(len(employee_unactive_res.json()['data'])):
                # for i in range(len(mobile)):
                mobile.append(employee_unactive_res.json()['data'][i]['mobile'])

                # 获取flow_id
                flow_id_res = Muscat(setup_class[0]).get_flow_id()

                # 发送验证码
                data['vcode']['headers']['x-flow-id'] = flow_id_res.json()['data']
                data['vcode']['params']['mobile_number'] = mobile[i]
                vcode_res = Muscat(setup_class[0]).vcode_api(data['vcode'])
                Assertions().assert_mode(vcode_res, data['vcode'])

                # 校验验证码
                data['vcode_check']['headers']['x-flow-id'] = flow_id_res.json()['data']
                data['vcode_check']['params']['mobile_number'] = mobile[i]
                vcode_check_res = Muscat(setup_class[0]).vcode_check_api(data['vcode_check'])
                Assertions().assert_mode(vcode_check_res, data['vcode_check'])

                # 校验员工是否能够通过链接加入到公司
                data['check']['params']['mobile'] = mobile[i]
                data['check']['params']['companyId'] = setup_class[1]
                check_active_mobile_res = WorkforceEmployeeDomain(setup_class[0]).check_active_mobile(data['check'])
                Assertions().assert_mode(check_active_mobile_res, data['check'])

                # NEED_ACTIVE类型的员工未注册登陆过，所以需要设置密码
                if check_active_mobile_res.json()['data'] == 'NEED_ACTIVE':

                    # 注册激活员工（设置密码）
                    data['employee_register']['body']['mobile'] = mobile[i]
                    active_employee_register_res = ThirdSysUserApi(setup_class[0]).test_active_employee_register(
                        data['employee_register'])
                    Assertions().assert_mode(active_employee_register_res, data['employee_register'])

                    # 激活员工
                    data['employee_active']['params']['mobile'] = mobile[i]
                    data['employee_active']['params']['companyId'] = setup_class[1]
                    employee_active_res = WorkforceEmployeeDomain(setup_class[0]).invitation_active_employee(
                        data['employee_active'])
                    Assertions().assert_mode(employee_active_res, data['employee_active'])

                # EXIST_ACTIVE类型的员工已经注册过系统，设置过密码，所以不需要再次设置密码，只需要在对应公司进行激活操作
                elif check_active_mobile_res.json()['data'] == 'EXIST_ACTIVE':

                    # 激活员工
                    data['employee_active']['params']['mobile'] = mobile[i]
                    data['employee_active']['params']['companyId'] = setup_class[1]
                    employee_active_res = WorkforceEmployeeDomain(setup_class[0]).invitation_active_employee(
                        data['employee_active'])
                    Assertions().assert_mode(employee_active_res, data['employee_active'])

                    # 查询数据库激活状态是否成功
                    select_active_status = "select * from employee where user_id is not null and mobile = %s " % (
                        mobile[i])
                    select_result = mysql_operate_select_fetchone('bipo_lite_dktest3', select_active_status)
                    if select_result is not None:
                        pass
                    else:
                        print("员工激活失败======================")

                else:
                    continue
        else:
            print("当前公司不存在未激活员工数据")


if __name__ == '__main__':
    pytest.main(['-sv', 'test_employee_manager_activate.py', '--env', 'test3'])
