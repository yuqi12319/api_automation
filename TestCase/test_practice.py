# coding:utf-8
# Name:test_practice.py
# Author:qi.yu
# Time:2020/9/8 10:37 上午
# Description:

import Common.consts
import pytest
from Common.request import Request


class TestPractice:

    @pytest.mark.skip
    def test_add_condition_approval(self):
        url = 'http://dktest3-workio.bipocloud.com/services/dukang-workflow/api/workflow_setting'
        headers = dict()
        headers['X-Dk-Token'] = Common.consts.ACCESS_TOKEN[0]
        workflowSettingRuleGroupDtoList = list()
        workflowSettingRuleGroupDtoList.append({
            'workflowSettingApproverList': [],
            'workflowSettingCcList': ['733358092208570368'],
            'workflowSettingRuleGroupRuleDtoList': [
                {
                    'ruleName': 'REQUIRE_APPROVAL',
                    'ruleValue': 0
                }
            ]
        })
        # print(workflowSettingRuleGroupDtoList)
        recruitment_type = ['', 'New', 'Replacement']
        finance = ['', 'LessThan', 'GreaterThan', 'EqualTo', 'LessThanEqualTo', 'GreaterThanEqualTo']
        personnel = ['', 'LessThan', 'GreaterThan', 'EqualTo', 'LessThanEqualTo', 'GreaterThanEqualTo']

        # body = {
        #     'coOrgId': Common.consts.COMPANY_ID,
        #     'name': '申请审批流test03',
        #     'orgIds': ['745673358925889536'],
        #     'type': 'WORKFORCEAPPLICATION',
        #     'workflowSettingId': 742749943449518080,
        #     'workflowSettingRuleGroupDtoList': 1
        # }

    def test_approval(self):
        url = 'http://dktest3-workio.bipocloud.com/services/dukang-workflow/api/organizations/745674007805689856/workflow/approval/query'
        headers = dict()
        headers['X-Dk-Token'] = Common.consts.ACCESS_TOKEN[0]
        body = {
            'employeeId': '733358092208570368',
            'type': 'WORKFORCEAPPLICATION',
            'workforceApplicationDto': {
                'coOrgId': '733358092246319104',
                'financeActual': 100,
                'financePlan': 101,
                'organizationId': "745674007805689856",
                'personnelActual': 7,
                'personnelPlan': 6,
                'recruitmentType': "New"
            }
        }
        res = Request().send_request_method('post', url=url, json=body, headers=headers)
        print(res.json()['data']['employeeVoList'][1]['displayName'],res.json()['data']['employeeVoList'][2]['displayName'])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_practice.py'])
