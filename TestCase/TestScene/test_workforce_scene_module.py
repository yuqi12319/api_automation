# coding:utf-8
# Name:test_workforce_scene_module.py
# Author:qi.yu
# Time:2020/7/29 3:25 下午
# Description:劳务工场景case

import pytest, allure, time, datetime
import Common.consts
from Common.operation_yaml import YamlHandle
from Common.operation_assert import Assertions
from Common.operation_mysql import *
from Common.log import MyLog
from TestApi.CommissionApi.positon import Position
from TestApi.EmployeeApi.employee_api import EmployeeApi
from TestApi.WorkforceApi.workforce_apply import WorkforceApply
from TestApi.WorkforceApi.workforce_require import WorkforceRequire
from TestApi.MuscatApi.muscat import Muscat
from TestApi.CocApi.coc import Coc
from TestApi.CommissionApi.commission import Commission
from TestApi.WorkflowApi.workflow_domain import WorkflowDomain
from TestApi.EmployeeApi.workforce_employee_domain import WorkforceEmployeeDomain
from TestApi.WorkforceApi.workforce_dispatch import WorkforceDispatch
from TestApi.WorkforceApi.workforce_receive import WorkforceRecevice
from TestApi.WorkflowApi.workflow_set_api import WorkflowSetApi
from TestApi.ContingentProjectApi.contingent_project import ContingentProject
from TestApi.EmployeeApi.workforce_employee_domain import WorkforceEmployeeDomain


@allure.feature("劳务工场景测试")
class TestWorkforceScene:

    @pytest.fixture(scope='class')
    def setup_class(self, env):
        company_id = str()
        company_name = str()
        employee_id = str()
        data_dict = dict()
        data_dict['env'] = env
        if Common.consts.COMPANY_INFORMATION:
            company_id = Common.consts.COMPANY_INFORMATION[0]['company_id']
            employee_id = Common.consts.COMPANY_INFORMATION[0]['employee_id']
        else:
            my_companies_res = Muscat(env).get_my_companies_api()
            if my_companies_res.json()['data']:
                company_id = my_companies_res.json()['data'][-1]['company_id']
                company_name = my_companies_res.json()['data'][-1]['company_name']
                brief_profile_data = YamlHandle().read_yaml('SingleInterfaceData/Employee/brief_profile.yaml')[0]
                brief_profile_data['params']['company_id'] = company_id
                brief_profile_res = EmployeeApi(env).brief_profile_api(brief_profile_data)
                employee_id = brief_profile_res.json()['data']['employee_id']
            else:
                MyLog().error('当前用户下没有公司列表')
        data_dict['company_id'] = company_id
        data_dict['company_name'] = company_name
        data_dict['employee_id'] = employee_id

        # 判断当前公司是否有关联劳务公司
        workforce_cmpany_map_data = YamlHandle().read_yaml('SingleInterfaceData/Coc/workforce_company_map.yaml')[0]
        workforce_cmpany_map_data['params']['coOrgId'] = company_id
        workforce_company_map_res = Coc(env).workforce_company_map_api(workforce_cmpany_map_data)
        data_dict['workforce_company_map'] = dict()
        if workforce_company_map_res.json()['data']:
            data_dict['workforce_company_map']['labourCompanyId'] = workforce_company_map_res.json()['data'][0][
                'workforceCompanyId']
            data_dict['workforce_company_map']['labourCompanyName'] = workforce_company_map_res.json()['data'][0][
                'workforceCompanyName']
            MyLog().info('关联劳务公司' + workforce_company_map_res.text)
        else:
            MyLog().debug('当前公司没有关联劳务公司')
            add_workforce_company_map_data = YamlHandle().read_yaml('SingleInterfaceData/Coc/workforce_company_relation_add.yaml')[0]
            add_workforce_company_map_data['body']['coOrgId'] = company_id
            add_workforce_company_map_data['body']['workforceCoOrgId'] = company_id
            Coc(env).workforce_company_workforce_add(add_workforce_company_map_data)
            data_dict['workforce_company_map']['labourCompanyId'] = company_id
            data_dict['workforce_company_map']['labourCompanyName'] = company_name

        # 判断当前公司是否是职位信息
        positions_data = YamlHandle().read_yaml('SingleInterfaceData/Commission/position.yaml')[0]
        positions_data['body']['coOrgId'] = company_id
        positions_res = Commission(env).positions(positions_data)
        data_dict['position'] = dict()
        if positions_res.json()['data']['positionVoList']:
            data_dict['position']['positionId'] = positions_res.json()['data']['positionVoList'][0]['positionId']
            data_dict['position']['positionName'] = positions_res.json()['data']['positionVoList'][0]['name']
            MyLog().info('职位信息' + positions_res.text)
        else:
            MyLog().debug("当前公司没有职位信息")
            add_position = dict()
            add_position['body'] = dict()
            add_position['body']['coOrgId'] = self.company_id
            position_name = '职位' + str(int(time.time()))
            add_position['body']['name'] = position_name
            add_position_res = Position(self.env).add_position_api(add_position)
            data_dict['position']['positionId'] = add_position_res.json()['data']
            data_dict['position']['positionName'] = position_name

        # 判断是否有项目
        get_project_data = YamlHandle().read_yaml('SingleInterfaceData/ContingentProject/project.yaml')[0]
        get_project_data['params']['coOrgId'] = company_id
        get_project_data['body']['coOrgId'] = company_id
        get_project_data_res = ContingentProject(env).get_project_list_api(get_project_data)
        data_dict['project'] = dict()
        if get_project_data_res.json()['data']['list']:
            data_dict['project']['id'] = get_project_data_res.json()['data']['list'][0]['id']
            data_dict['project']['name'] = get_project_data_res.json()['data']['list'][0]['name']
            MyLog().info('项目信息' + get_project_data_res.text)
        else:
            MyLog().debug('当前公司没有项目')
            add_project_data = dict()
            add_project_data['body'] = dict()
            add_project_data['body']['coOrgId'] = company_id
            add_project_data['body']['code'] = str(int(time.time()))
            project_name = '项目' + str(int(time.time()))
            add_project_data['body']['name'] = project_name
            add_project_res = ContingentProject(env).add_project_api(add_project_data)
            data_dict['project']['id'] = add_project_res.json()['data']
            data_dict['project']['name'] = project_name

        # 判断当前公司是否有组织架构
        organizations_trees_data = YamlHandle().read_yaml('SingleInterfaceData/Muscat/organizations.yaml')[0]
        organizations_trees_data['employeeid'] = employee_id
        organizations_trees_data['params']['coOrgId'] = company_id
        organizations_trees_res = Muscat(env).organizations(organizations_trees_data)
        data_dict['organizations_trees'] = dict()
        data_dict['organizations_trees']['organizationId'] = organizations_trees_res.json()['data'][0]['id']
        data_dict['organizations_trees']['organizationName'] = organizations_trees_res.json()['data'][0]['name']

        # 根据组织架构节点获取对应审批流
        approval_data = YamlHandle().read_yaml('SingleInterfaceData/Workflow/workflow_approval_query.yaml')[0]
        approval_data['organizationId'] = organizations_trees_res.json()['data'][0]['id']
        approval_data['body']['employeeId'] = employee_id
        approval_data['body']['type'] = 'WORKFORCEAPPLICATION'
        approval_res = WorkflowDomain(env).workflow_approval_query(approval_data)
        data_dict['approval'] = dict()
        data_dict['approval']['workflowDeploymentId'] = approval_res.json()['data']['workflowDeploymentId']

        return data_dict

    @pytest.mark.skip
    @allure.story("主流程")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/main_scene.yaml'))
    def test_main_scene(self, data, setup_class):
        # with allure.step('第一步：设置申请审批流,无需审批'):
        #     # 获取默认用工申请审批流
        #     data['workforce_application_approval_list']['params']['coOrgId'] = setup_class['company_id']
        #     workforce_application_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
        #         data['workforce_application_approval_list'])
        #     Assertions().assert_mode(workforce_application_approval_list_res,
        #                              data['workforce_application_approval_list'])
        #     for item in workforce_application_approval_list_res.json()['data']['workflowSettingVoList']:
        #         if item['name'] == '默认用工申请审批流':
        #             default_workforce_application_approval = item
        #
        #     # 修改默认用工申请审批流无需审批
        #     data['update_default_approval']['body']['coOrgId'] = setup_class['company_id']
        #     data['update_default_approval']['body']['orgIds'].append(setup_class['company_id'])
        #     data['update_default_approval']['body']['workflowSettingId'] = default_workforce_application_approval[
        #         'workflowSettingId']
        #     update_default_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
        #         data['update_default_approval'])
        #     Assertions().assert_mode(update_default_approval_res, data['update_default_approval'])

        with allure.step('第一步：发送申请单'):
            # 数据拼接
            data['send_apply']['body']['coOrgId'] = setup_class['company_id']
            data['send_apply']['body']['coOrgName'] = setup_class['company_name']
            data['send_apply']['body']['labourCompanyId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['send_apply']['body']['labourCompanyName'] = setup_class['workforce_company_map']['labourCompanyName']
            data['send_apply']['body']['organizationId'] = setup_class['organizations_trees']['organizationId']
            data['send_apply']['body']['organizationName'] = setup_class['organizations_trees']['organizationName']
            data['send_apply']['body']['positionId'] = setup_class['position']['positionId']
            data['send_apply']['body']['positionName'] = setup_class['position']['positionName']
            data['send_apply']['body']['projectId'] = setup_class['project']['id']
            data['send_apply']['body']['projectName'] = setup_class['project']['name']
            data['send_apply']['body']['joinDate'] = round(int(time.mktime(datetime.date.today().timetuple()))*1000)
            data['send_apply']['body']['probationPeriodExpire'] = round(int(time.mktime(datetime.date.today().timetuple()))*1000)
            data['send_apply']['body']['workflowDeploymentId'] = setup_class['approval']['workflowDeploymentId']
            data['send_apply']['body']['applyEmployeeId'] = setup_class['employee_id']
            send_apply_res = WorkforceApply(setup_class['env']).send_apply_api(data['send_apply'])
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        # with allure.step('第二步：获取申请列表'):
        #     apply_list_res = WorkforceApply(self.env).apply_list_api(data['apply_list'])
        #     Assertions().assert_code(apply_list_res.status_code, 200)
        #     Assertions().assert_in_text(apply_list_res.json()['data'], str(data['send_apply']['body']['joinDate']))
        #     for item in apply_list_res.json()['data']:
        #         if item['joinDate'] == data['send_apply']['body']['joinDate']:
        #             code = item['code']  # 获取申请id
        #             break
        #
        # with allure.step('第三步：获取需求列表'):
        #     require_list_res = WorkforceRequire(self.env).require_list_api(data['require_list'])
        #     Assertions().assert_code(require_list_res.status_code, 200)
        #     Assertions().assert_in_text(require_list_res.json()['data'], str(code))
        #
        # def clear_data():  # 场景执行完毕清理数据操作
        #     delete_apply_sql = "DELETE FROM workforce_application WHERE `code` = %s" % code
        #     mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_apply_sql)
        #     delete_require_sql = "DELETE FROM workforce_ticket WHERE `code` = %s" % code
        #     mysql_operate_insert_update_delete('dukang_workforce_dktest3', delete_sql=delete_require_sql)
        #
        # clear_data()

    @pytest.mark.skip
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
            data['free_employee']['body']['beginTime'] = require_detail_res.json()['data']['organization'][
                'expectJoinDate']
            data['free_employee']['body']['endTime'] = require_detail_res.json()['data']['organization'][
                'probationPeriodExpire']
            data['free_employee']['body']['coOrgId'] = precondition['workforce_company_map'][0][
                'workforceCompanyId']
            workforce_employees_free_res = WorkforceEmployeeDomain(self.env).workforce_employees_free(
                data['free_employee'])
            Assertions().assert_mode(workforce_employees_free_res, data['free_employee'])

        with allure.step('第十步：乙方根据需求单派遣一个员工'):
            data['dispatch']['body']['beginTime'] = require_detail_res.json()['data']['organization']['expectJoinDate']
            data['dispatch']['body']['endTime'] = require_detail_res.json()['data']['organization'][
                'probationPeriodExpire']
            data['dispatch']['body']['coOrgId'] = require_detail_res.json()['data']['coOrgId']['companyId']
            data['dispatch']['body']['dispatchCoOrgId'] = require_detail_res.json()['data']['demandCompany'][
                'companyId']
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

    @pytest.mark.skip
    def test_a(self, setup_class):
        workforce_employees_free_data = dict()
        workforce_employees_free_data['params'] = dict()
        workforce_employees_free_data['body'] = dict()
        workforce_employees_free_data['params']['page'] = 0
        workforce_employees_free_data['params']['size'] = 20
        workforce_employees_free_data['body']['beginTime'] = 1600790400000
        workforce_employees_free_data['body']['endTime'] = 1600790400000
        workforce_employees_free_data['body']['coOrgId'] = 758029363823247360
        workforce_employees_free_data['body']['name'] = ''
        workforce_employees_free_res = WorkforceEmployeeDomain(setup_class['env']).workforce_employees_free(workforce_employees_free_data)
        employee = workforce_employees_free_res.json()['data'][1]['id']

        dispatch_data = dict()
        dispatch_data['body'] = dict()
        dispatch_data['body']['beginTime'] = 1600790400000
        dispatch_data['body']['coOrgId'] = 758029363823247360
        dispatch_data['body']['dispatchCoOrgId'] = 758029363823247360
        dispatch_data['body']['endTime'] = 1600790400000
        dispatch_data['body']['workforceRequestId'] = 758359950903738368
        employeeIds = list()
        employeeIds.append(employee)
        dispatch_data['body']['employeeIds'] = employeeIds
        dispatch_res = WorkforceDispatch(setup_class['env']).dispatch_api(dispatch_data)

    @pytest.mark.skip
    def test_b(self, setup_class):
        recevice_list_data = dict()
        recevice_list_data['params'] = dict()
        recevice_list_data['params']['coOrgId'] = setup_class['company_id']
        recevice_list_data['params']['offset'] = 900
        recevice_list_data['params']['limit'] = 100
        recevice_list_res = WorkforceRecevice(setup_class['env']).recevice_list_api(recevice_list_data)

        for item in recevice_list_res.json()['data']:
            recevice_detail_data = dict()
            recevice_detail_data['params'] = dict()
            recevice_detail_data['params']['ticketId'] = item['ticketId']
            recevice_detail_data['params']['workforceWorkingAssignId'] = item['workforceWorkingAssignId']
            recevice_detail_res = WorkforceRecevice(setup_class['env']).recevice_detail_api(recevice_detail_data)

            agree_recevice_data = dict()
            agree_recevice_data['body'] = dict()
            agree_recevice_data['body']['beginTime'] = 1600790400000
            agree_recevice_data['body']['coOrgId'] = setup_class['company_id']
            agree_recevice_data['body']['endTime'] = 1600790400000
            agree_recevice_data['body']['ticketId'] = item['ticketId']
            agree_recevice_data['body']['workforceWorkingAssignId'] = item['workforceWorkingAssignId']
            employeeCompanyDtos = list()
            employeeCompanyDto = dict()
            employeeCompanyDto['coOrgId'] = setup_class['company_id']
            employeeCompanyDto['employeeId'] = recevice_detail_res.json()['data']['workforceEmployeeManageVos'][0]['id']
            employeeCompanyDtos.append(employeeCompanyDto)
            agree_recevice_data['body']['employeeCompanyDtos'] = employeeCompanyDtos
            WorkforceRecevice(setup_class['env']).agree_recevice_api(agree_recevice_data)


if __name__ == '__main__':
    # for i in range(994):
    pytest.main(["-sv", "test_workforce_scene_module.py::TestWorkforceScene::test_b", "--env", "test3"])
