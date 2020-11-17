# coding:utf-8
# Name:test_demo.py
# Author:qi.yu
# Time:2020/11/12 11:40 上午
# Description:
import pytest

from TestApi.CocApi.company_register_request_api import CompanyRegisterRequestApi
from TestApi.CocApi.company_workforce_map_api import CompanyWorkforceMapApi


class TestDemo:
    # 审核注册公司
    def test_audit_company(self, env, id):
        data = dict()
        data['body'] = dict()
        data['body']['id'] = id
        data['body']['approvalStatus'] = 'AGREED'
        company_register_approval_res = CompanyRegisterRequestApi(env).company_register_approval_api(
            data)
        print(company_register_approval_res.json())

    # 劳务公司关联
    def test_workforce_company_map(self, env, coOrgId, workforceCoOrgId):
        data = dict()
        data['body'] = dict()
        data['body']['coOrgId'] = coOrgId
        data['body']['workforceCoOrgId'] = workforceCoOrgId
        workforce_company_workforce_add_res = CompanyWorkforceMapApi(env).workforce_company_workforce_add_api(data)
        print(workforce_company_workforce_add_res.json())


if __name__ == '__main__':
    pytest.main(["-sv", "test_demo.py::TestDemo::test_audit_company", "--env", "online"])
