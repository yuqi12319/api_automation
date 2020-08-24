# coding:utf-8
# Name:test_workforce_scene_module.py
# Author:qi.yu
# Time:2020/7/29 3:25 下午
# Description:劳务工场景case

import pytest, allure
import Common.consts
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Common.operation_mysql import *
from Common import log
from TestApi.WorkforceApi.workforce_apply import WorkforceApply
from TestApi.WorkforceApi.workforce_require import WorkforceRequire
from TestApi.MuscatApi.muscat import Muscat
from TestApi.CocApi.coc import Coc
from TestApi.CommissionApi.commission import Commission
from TestApi.ContingentProjectApi.contingent_project import ContingentProject
from TestApi.WorkflowApi.workflow_domain import WorkflowDomain
from TestApi.EmployeeApi.workforce_employee_domain import WorkforceEmployeeDomain
from TestApi.WorkforceApi.workforce_dispatch import WorkforceDispatch
from TestApi.WorkforceApi.workforce_receive import WorkforceRecevice


@allure.feature("劳务工场景测试")
class TestWorkforceScene:

    @pytest.fixture(autouse=True)
    def precondition(self, env):
        self.env = env
        self.log = log.MyLog()
        headers = dict()
        headers['X-Dk-Token'] = Common.consts.ACCESS_TOKEN[0]
        my_companies_res = Muscat(env).get_my_companies_api()
        for item in my_companies_res.json()['data']:
            data_dict = dict()
            data_dict['my_company'] = item
            # 判断当前公司是否有关联劳务公司
            workforce_company_map_data = YamlHandle().read_yaml('SingleInterfaceData/Coc/workforce_company_map.yaml')[0]
            workforce_company_map_data['params']['coOrgId'] = item['company_id']
            workforce_company_map_res = Coc(env).workforce_company_map_api(workforce_company_map_data)
            if workforce_company_map_res.json()['data']:
                data_dict['workforce_company_map'] = workforce_company_map_res.json()['data']
            else:
                continue

            # 判断当前公司是否是职位信息
            positions_data = YamlHandle().read_yaml('SingleInterfaceData/Commission/position.yaml')[0]
            positions_data['body']['coOrgId'] = item['company_id']
            positions_res = Commission(env).positions(positions_data)
            if positions_res.json()['data']:
                data_dict['position'] = positions_res.json()['data']
            else:
                self.log.error("当前公司没有职位信息")
                continue

            # 获取当前员工id
            employeeid_data = YamlHandle().read_yaml('SingleInterfaceData/Muscat/company_guide_employeeid.yaml')[0]
            employeeid_data['params']['company_id'] = item['company_id']
            employeeid_res = Muscat(env).company_guide_employeeid(employeeid_data)
            data_dict['employee'] = employeeid_res.json()['data']

            # 判断当前公司是否有组织架构
            organizations_trees_data = YamlHandle().read_yaml('SingleInterfaceData/Muscat/organizations.yaml')[0]
            organizations_trees_data['employeeid'] = employeeid_res.json()['data']
            organizations_trees_data['params']['coOrgId'] = item['company_id']
            organizations_trees_res = Muscat(env).organizations(organizations_trees_data)
            if organizations_trees_res.json()['data']:
                data_dict['organizations_trees'] = organizations_trees_res.json()['data']
            else:
                continue

            # 根据组织架构节点获取对应审批流
            approval_data = YamlHandle().read_yaml('SingleInterfaceData/Workflow/workflow_approval_query.yaml')[0]
            approval_data['organizationId'] = organizations_trees_res.json()['data'][0]['id']
            approval_data['body']['employeeId'] = employeeid_res.json()['data']
            approval_data['body']['type'] = 'WORKFORCEAPPLICATION'
            approval_res = WorkflowDomain(env).workflow_approval_query(approval_data)
            data_dict['approval'] = approval_res.json()['data']

            # 判断是否有项目
            project_data = YamlHandle().read_yaml('SingleInterfaceData/ContingentProject/project.yaml')[0]
            project_data['params']['coOrgId'] = item['company_id']
            project_data['body']['coOrgId'] = item['company_id']
            project_res = ContingentProject(env).project(project_data)
            if project_res.json()['data']:
                data_dict['project'] = project_res.json()['data']['list'][0]
            return data_dict

    @pytest.mark.skip
    @allure.story("主流程")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/main_scene.yaml'))
    def test_main_scene(self, data, precondition):
        data_dict = self.precondition()
        with allure.step('第一步：发送申请单'):
            # 数据拼接
            data['send_apply']['body']['coOrgId'] = data_dict['my_company']['company_id']
            data['send_apply']['body']['coOrgName'] = data_dict['my_company']['company_name']
            data['send_apply']['body']['labourCompanyId'] = data_dict['workforce_company_map'][0][
                'workforceCompanyId']
            data['send_apply']['body']['labourCompanyName'] = data_dict['workforce_company_map'][0][
                'workforceCompanyName']
            data['send_apply']['body']['organizationId'] = data_dict['organizations_trees'][0]['id']
            data['send_apply']['body']['organizationName'] = data_dict['organizations_trees'][0]['name']
            data['send_apply']['body']['positionId'] = data_dict['position']['positionVoList'][0][
                'positionId']
            data['send_apply']['body']['positionName'] = data_dict['position']['positionVoList'][0]['name']
            data['send_apply']['body']['applyEmployeeId'] = data_dict['employee']
            employeeVoList = data_dict['approval']['employeeVoList']
            del (employeeVoList[0])
            for approver in employeeVoList:
                approver['employeeId'] = approver['id']
            data['send_apply']['body']['approverList'] = employeeVoList
            new_ccVoList = []
            ccVoList = data_dict['approval']['ccVoList']
            for ccVo in ccVoList:
                new_ccVoList.append(ccVo['employeeId'])
            data['send_apply']['body']['ccList'] = new_ccVoList
            data['send_apply']['body']['workflowDeploymentId'] = data_dict['approval']['workflowDeploymentId']
            # data['send_apply']['body']['joinDate'] =
            # data['send_apply']['body']['probationPeriodExpire'] =
            send_apply_res = WorkforceApply(self.env).send_apply_api(data['send_apply'])
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表'):
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    break

        with allure.step('第三步：获取需求列表'):
            require_list_res = WorkforceRequire(self.env).require_list_api(data['require_list'])
            Assertions().assert_code(require_list_res.status_code, 200)
            Assertions().assert_in_text(require_list_res.json()['data'], str(code))

        def clear_data():  # 场景执行完毕清理数据操作
            delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
            delete_require_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % code
            mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_require_sql)

        clear_data()

    # @pytest.mark.skip
    @allure.story("撤销申请")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/withdraw_apply.yaml'))
    def test_withdraw_apply(self, data, precondition):

        with allure.step('第一步：发送申请单'):
            # 数据拼接
            data['send_apply']['body']['coOrgId'] = precondition['my_company']['company_id']
            data['send_apply']['body']['coOrgName'] = precondition['my_company']['company_name']
            data['send_apply']['body']['labourCompanyId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            data['send_apply']['body']['labourCompanyName'] = precondition['workforce_company_map'][0][
                'workforceCompanyName']
            data['send_apply']['body']['organizationId'] = precondition['organizations_trees'][0]['id']
            data['send_apply']['body']['organizationName'] = precondition['organizations_trees'][0]['name']
            data['send_apply']['body']['positionId'] = precondition['position']['positionVoList'][0][
                'positionId']
            data['send_apply']['body']['positionName'] = precondition['position']['positionVoList'][0]['name']
            data['send_apply']['body']['projectId'] = precondition['project']['id']
            data['send_apply']['body']['projectName'] = precondition['project']['name']
            data['send_apply']['body']['applyEmployeeId'] = precondition['employee']
            employeeVoList = precondition['approval']['employeeVoList']
            del (employeeVoList[0])
            for approver in employeeVoList:
                approver['employeeId'] = approver['id']
            data['send_apply']['body']['approverList'] = employeeVoList
            new_ccVoList = []
            ccVoList = precondition['approval']['ccVoList']
            for ccVo in ccVoList:
                new_ccVoList.append(ccVo['employeeId'])
            data['send_apply']['body']['ccList'] = new_ccVoList
            data['send_apply']['body']['workflowDeploymentId'] = precondition['approval']['workflowDeploymentId']
            # data['send_apply']['body']['joinDate'] =
            # data['send_apply']['body']['probationPeriodExpire'] =
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            send_apply_res = WorkforceApply(self.env).send_apply_api(data['send_apply'])
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表,判断是否有当前申请单'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    application_id = item['applicationId']
                    break

        with allure.step('第三步：获取申请单详情'):
            data['apply_detail']['application_id'] = application_id
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            apply_detail_res = WorkforceApply(self.env).apply_detail_api(data['apply_detail'])
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])

        with allure.step('第四步：撤销当前申请单'):
            data['withdraw_apply']['application_id'] = application_id
            data['withdraw_apply']['body']['form_workflow_id'] = apply_detail_res.json()['data']['formWorkflowId']
            data['withdraw_apply']['body']['process_instance_id'] = apply_detail_res.json()['data']['processInstanceId']
            allure.attach(str(data['withdraw_apply']), "请求数据", allure.attachment_type.JSON)
            withdraw_apply_res = WorkforceApply(self.env).withdraw_apply_api(data['withdraw_apply'])
            allure.attach(withdraw_apply_res.text, "withdraw_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(withdraw_apply_res, data['withdraw_apply'])

        with allure.step('第五步：获取申请列表,判断当前申请单状态是否变更为已撤销'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'ROLLBACK')
                    break

        # def clear_data():  # 场景执行完毕清理数据操作
        #     delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
        #     mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
        #
        # clear_data()

    @pytest.mark.skip
    @allure.story("停止申请")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/stop_apply.yaml'))
    def test_stop_apply(self, data, precondition):

        with allure.step('第一步：发送申请单'):
            # 数据拼接
            data['send_apply']['body']['coOrgId'] = precondition['my_company']['company_id']
            data['send_apply']['body']['coOrgName'] = precondition['my_company']['company_name']
            data['send_apply']['body']['labourCompanyId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            data['send_apply']['body']['labourCompanyName'] = precondition['workforce_company_map'][0][
                'workforceCompanyName']
            data['send_apply']['body']['organizationId'] = precondition['organizations_trees'][0]['id']
            data['send_apply']['body']['organizationName'] = precondition['organizations_trees'][0]['name']
            data['send_apply']['body']['positionId'] = precondition['position']['positionVoList'][0][
                'positionId']
            data['send_apply']['body']['positionName'] = precondition['position']['positionVoList'][0]['name']
            data['send_apply']['body']['projectId'] = precondition['project']['id']
            data['send_apply']['body']['projectName'] = precondition['project']['name']
            data['send_apply']['body']['applyEmployeeId'] = precondition['employee']
            employeeVoList = precondition['approval']['employeeVoList']
            del (employeeVoList[0])
            for approver in employeeVoList:
                approver['employeeId'] = approver['id']
            data['send_apply']['body']['approverList'] = employeeVoList
            new_ccVoList = []
            ccVoList = precondition['approval']['ccVoList']
            for ccVo in ccVoList:
                new_ccVoList.append(ccVo['employeeId'])
            data['send_apply']['body']['ccList'] = new_ccVoList
            data['send_apply']['body']['workflowDeploymentId'] = precondition['approval']['workflowDeploymentId']
            # data['send_apply']['body']['joinDate'] =
            # data['send_apply']['body']['probationPeriodExpire'] =
            # print(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            send_apply_res = WorkforceApply(self.env).send_apply_api(data['send_apply'])
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表,判断是否有当前申请单'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    application_id = item['applicationId']
                    break

        with allure.step('第三步：获取申请单详情'):
            data['apply_detail']['application_id'] = application_id
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            apply_detail_res = WorkforceApply(self.env).apply_detail_api(data['apply_detail'])
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])

        with allure.step('第四步：审批流通过'):
            data['approve_node']['body']['employeeId'] = employeeVoList[0]['id']
            data['approve_node']['body']['formId'] = apply_detail_res.json()['data']['workforceApplicationId']
            data['approve_node']['body']['formWorkflowId'] = apply_detail_res.json()['data']['formWorkflowId']
            data['approve_node']['body']['processInstanceId'] = apply_detail_res.json()['data']['processInstanceId']
            allure.attach(str(data['approve_node']), "请求数据", allure.attachment_type.JSON)
            approve_res = WorkflowDomain(self.env).workflow_node_approve_api(data['approve_node'])
            allure.attach(approve_res.text, "workflow_node_approve_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(approve_res, data['approve_node'])

        with allure.step('第五步：获取申请列表，判断当前申请单状态是否变更为已通过'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'AGREED')
                    break

        with allure.step('第六步：获取需求列表，判断乙方是否对应生成需求单'):
            data['require_list']['body']['coOrgId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            allure.attach(str(data['require_list']), "请求数据", allure.attachment_type.JSON)
            require_list_res = WorkforceRequire(self.env).require_list_api(data['require_list'])
            allure.attach(require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(require_list_res.status_code, 200)
            Assertions().assert_in_text(require_list_res.json(), str(code))

        with allure.step('第七步：停止用工申请'):
            data['stop_apply']['application_id'] = application_id
            allure.attach(str(data['stop_apply']), "请求数据", allure.attachment_type.JSON)
            stop_apply_res = WorkforceApply(self.env).stop_apply_api(data['stop_apply'])
            allure.attach(stop_apply_res.text, "stop_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(stop_apply_res, data['stop_apply'])

        with allure.step('第八步：重新获取申请列表，判断当前订单状态是否已停止'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'STOP')
                    break

        with allure.step('第九步：重新获取需求列表，判断当前订单状态是否已停止'):
            data['require_list']['body']['coOrgId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            allure.attach(str(data['require_list']), "请求数据", allure.attachment_type.JSON)
            require_list_res = WorkforceRequire(self.env).require_list_api(data['require_list'])
            allure.attach(require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            for item in require_list_res.json()['data']:
                if item['applicationCode'] == code:
                    Assertions().assert_text(item['status'], 'STOP')
                    break

        # def clear_data():  # 场景执行完毕清理数据操作
        #     delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
        #     mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
        #     delete_require_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % code
        #     mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_require_sql)

        # clear_data()

    @pytest.mark.skip
    @allure.story("拒绝申请(申请审批流拒绝)")
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('SceneData/WorkforceScene/refuse_apply_approve.yaml'))
    def test_refuse_apply_approve(self, data, precondition):

        with allure.step('第一步：发送申请单'):
            # 数据拼接
            data['send_apply']['body']['coOrgId'] = precondition['my_company']['company_id']
            data['send_apply']['body']['coOrgName'] = precondition['my_company']['company_name']
            data['send_apply']['body']['labourCompanyId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            data['send_apply']['body']['labourCompanyName'] = precondition['workforce_company_map'][0][
                'workforceCompanyName']
            data['send_apply']['body']['organizationId'] = precondition['organizations_trees'][0]['id']
            data['send_apply']['body']['organizationName'] = precondition['organizations_trees'][0]['name']
            data['send_apply']['body']['positionId'] = precondition['position']['positionVoList'][0][
                'positionId']
            data['send_apply']['body']['positionName'] = precondition['position']['positionVoList'][0]['name']
            data['send_apply']['body']['projectId'] = precondition['project']['id']
            data['send_apply']['body']['projectName'] = precondition['project']['name']
            data['send_apply']['body']['applyEmployeeId'] = precondition['employee']
            employeeVoList = precondition['approval']['employeeVoList']
            del (employeeVoList[0])
            for approver in employeeVoList:
                approver['employeeId'] = approver['id']
            data['send_apply']['body']['approverList'] = employeeVoList
            new_ccVoList = []
            ccVoList = precondition['approval']['ccVoList']
            for ccVo in ccVoList:
                new_ccVoList.append(ccVo['employeeId'])
            data['send_apply']['body']['ccList'] = new_ccVoList
            data['send_apply']['body']['workflowDeploymentId'] = precondition['approval']['workflowDeploymentId']
            # data['send_apply']['body']['joinDate'] =
            # data['send_apply']['body']['probationPeriodExpire'] =
            # print(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            send_apply_res = WorkforceApply(self.env).send_apply_api(data['send_apply'])
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表,判断是否有当前申请单'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    application_id = item['applicationId']
                    break

        with allure.step('第三步：获取申请单详情'):
            data['apply_detail']['application_id'] = application_id
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            apply_detail_res = WorkforceApply(self.env).apply_detail_api(data['apply_detail'])
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])

        with allure.step('第四步：审批流拒绝'):
            data['approve_node']['body']['employeeId'] = employeeVoList[0]['id']
            data['approve_node']['body']['formId'] = apply_detail_res.json()['data']['workforceApplicationId']
            data['approve_node']['body']['formWorkflowId'] = apply_detail_res.json()['data']['formWorkflowId']
            data['approve_node']['body']['processInstanceId'] = apply_detail_res.json()['data']['processInstanceId']
            allure.attach(str(data['approve_node']), "请求数据", allure.attachment_type.JSON)
            approve_res = WorkflowDomain(self.env).workflow_node_approve_api(data['approve_node'])
            allure.attach(approve_res.text, "workflow_node_approve_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(approve_res, data['approve_node'])

        with allure.step('第五步：获取申请列表,判断当前申请单状态是否变更为已拒绝'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'REFUSED')
                    break

    @pytest.mark.skip
    @allure.story("拒绝接收")
    @pytest.mark.parametrize('data',
                             YamlHandle().read_yaml('SceneData/WorkforceScene/refuse_receive.yaml'))
    def test_refuse_register_approve(self, data, precondition):

        with allure.step('第一步：发送申请单'):
            # 数据拼接
            data['send_apply']['body']['coOrgId'] = precondition['my_company']['company_id']
            data['send_apply']['body']['coOrgName'] = precondition['my_company']['company_name']
            data['send_apply']['body']['labourCompanyId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            data['send_apply']['body']['labourCompanyName'] = precondition['workforce_company_map'][0][
                'workforceCompanyName']
            data['send_apply']['body']['organizationId'] = precondition['organizations_trees'][0]['id']
            data['send_apply']['body']['organizationName'] = precondition['organizations_trees'][0]['name']
            data['send_apply']['body']['positionId'] = precondition['position']['positionVoList'][0][
                'positionId']
            data['send_apply']['body']['positionName'] = precondition['position']['positionVoList'][0]['name']
            data['send_apply']['body']['projectId'] = precondition['project']['id']
            data['send_apply']['body']['projectName'] = precondition['project']['name']
            data['send_apply']['body']['applyEmployeeId'] = precondition['employee']
            employeeVoList = precondition['approval']['employeeVoList']
            del (employeeVoList[0])
            for approver in employeeVoList:
                approver['employeeId'] = approver['id']
            data['send_apply']['body']['approverList'] = employeeVoList
            new_ccVoList = []
            ccVoList = precondition['approval']['ccVoList']
            for ccVo in ccVoList:
                new_ccVoList.append(ccVo['employeeId'])
            data['send_apply']['body']['ccList'] = new_ccVoList
            data['send_apply']['body']['workflowDeploymentId'] = precondition['approval']['workflowDeploymentId']
            # data['send_apply']['body']['joinDate'] =
            # data['send_apply']['body']['probationPeriodExpire'] =
            # print(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            send_apply_res = WorkforceApply(self.env).send_apply_api(data['send_apply'])
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第二步：获取申请列表,判断是否有当前申请单'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(apply_list_res.status_code, 200)
            Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
            for item in apply_list_res.json()['data']:
                if item['joinDate'] == data['send_apply']['body']['joinDate']:
                    code = item['code']  # 获取申请id
                    application_id = item['applicationId']
                    break

        with allure.step('第三步：获取申请单详情'):
            data['apply_detail']['application_id'] = application_id
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            apply_detail_res = WorkforceApply(self.env).apply_detail_api(data['apply_detail'])
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])

        with allure.step('第四步：审批流通过'):
            data['approve_node']['body']['employeeId'] = employeeVoList[0]['id']
            data['approve_node']['body']['formId'] = apply_detail_res.json()['data']['workforceApplicationId']
            data['approve_node']['body']['formWorkflowId'] = apply_detail_res.json()['data']['formWorkflowId']
            data['approve_node']['body']['processInstanceId'] = apply_detail_res.json()['data']['processInstanceId']
            allure.attach(str(data['approve_node']), "请求数据", allure.attachment_type.JSON)
            approve_res = WorkflowDomain(self.env).workflow_node_approve_api(data['approve_node'])
            allure.attach(approve_res.text, "workflow_node_approve_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(approve_res, data['approve_node'])

        with allure.step('第五步：获取申请列表，判断当前申请单状态是否变更为已通过'):
            allure.attach(str(data['apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'AGREED')
                    break

        with allure.step('第六步：获取需求列表，判断乙方是否对应生成需求单'):
            data['require_list']['body']['coOrgId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            allure.attach(str(data['require_list']), "请求数据", allure.attachment_type.JSON)
            require_list_res = WorkforceRequire(self.env).require_list_api(data['require_list'])
            allure.attach(require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_code(require_list_res.status_code, 200)
            Assertions().assert_in_text(require_list_res.json(), str(code))
            for item in require_list_res.json()['data']:
                if item['applicationCode'] == code:
                    requirement_id = item['id']
                    break

        with allure.step('第七步：获取需求单详情'):
            data['require_detail']['applicationId'] = requirement_id
            allure.attach(str(data['require_detail']), "请求数据", allure.attachment_type.JSON)
            require_detail_res = WorkforceRequire(self.env).require_detail_api(data['require_detail'])
            allure.attach(require_list_res.text, "require_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(require_detail_res, data['require_detail'])

        with allure.step('第八步：获取关联申请,判断是否存在生成的需求单'):
            data['relevance_apply']['params']['coOrgId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            relevance_apply_res = WorkforceDispatch(self.env).relevance_apply_api(data['relevance_apply'])
            Assertions().assert_in_text(relevance_apply_res.json(), str(code))

        with allure.step('第九步：根据需求时间查询空闲员工'):
            data['free_employee']['body']['beginTime'] = require_detail_res.json()['data']['organization']['expectJoinDate']
            data['free_employee']['body']['endTime'] = require_detail_res.json()['data']['organization']['probationPeriodExpire']
            data['free_employee']['body']['coOrgId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            workforce_employees_free_res = WorkforceEmployeeDomain(self.env).workforce_employees_free(
                data['free_employee'])
            Assertions().assert_mode(workforce_employees_free_res, data['free_employee'])

        with allure.step('第十步：乙方根据需求单派遣一个员工'):
            data['dispatch']['body']['beginTime'] = require_detail_res.json()['data']['organization']['expectJoinDate']
            data['dispatch']['body']['endTime'] = require_detail_res.json()['data']['organization']['probationPeriodExpire']
            data['dispatch']['body']['coOrgId'] = require_detail_res.json()['data']['coOrgId']['companyId']
            data['dispatch']['body']['dispatchCoOrgId'] = require_detail_res.json()['data']['demandCompany']['companyId']
            data['dispatch']['body']['workforceRequestId'] = require_detail_res.json()['data']['id']
            data['dispatch']['body']['employeeIds'].append(workforce_employees_free_res.json()['data'][0]['id'])
            allure.attach(str(data['dispatch']), "请求数据", allure.attachment_type.JSON)
            dispatch_res = WorkforceDispatch(self.env).dispatch_api(data['dispatch'])
            allure.attach(require_list_res.text, "dispatch_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(dispatch_res, data['dispatch'])

        with allure.step('第十一步：获取接收列表，判断是否生成接收单'):
            data['recevice_list']['params']['coOrgId'] = precondition['my_company']['company_id']
            allure.attach(str(data['recevice_list']), "请求数据", allure.attachment_type.JSON)
            recevice_list_res = WorkforceRecevice(self.env).recevice_list_api(data['recevice_list'])
            allure.attach(require_list_res.text, "recevice_list_api返回结果", allure.attachment_type.JSON)
            # Assertions().assert_mode(recevice_list_res, )


if __name__ == '__main__':
    pytest.main(["-sv", "test_workforce_scene_module.py", "--env", "test3"])