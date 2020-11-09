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
from TestApi.WorkforceApi.workforce_ticket import WorkforceTicket
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
from TestApi.MuscatApi.department_api import DepartmentApi
from TestApi.WorkforceApi.workforce_workflow import WorkforceWorkflow
from TestCase.TestScene.organization import *
from TestApi.MuscatApi.organization_api import OrganizationApi
from TestApi.WorkflowApi.workflow_set_api import WorkflowSetApi
from TestCase.TestScene.test_import_employee_module import TestImportEmployee
from TestApi.WorkforceApi.workforce_register import WorkforceRegister
from TestApi.WorkforceApi.workforce_organization_api import WorkforceOrganizationApi
from TestApi.WorkforceApi.workforce_information_update_api import WorkforceInformationUpdateApi


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
            company_id = Common.consts.COMPANY_INFORMATION['company_id']
            company_name = Common.consts.COMPANY_INFORMATION['company_name']
            employee_id = Common.consts.COMPANY_INFORMATION['employee_id']
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
            add_workforce_company_map_data = \
                YamlHandle().read_yaml('SingleInterfaceData/Coc/workforce_company_relation_add.yaml')[0]
            add_workforce_company_map_data['body']['coOrgId'] = company_id
            add_workforce_company_map_data['body']['workforceCoOrgId'] = company_id
            add_workforce_company_map_res = Coc(env).workforce_company_workforce_add(add_workforce_company_map_data)
            Assertions().assert_code(add_workforce_company_map_res.status_code, 200)
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
            add_position['body']['coOrgId'] = company_id
            position_name = '职位' + str(int(time.time()))
            add_position['body']['name'] = position_name
            add_position_res = Position(env).add_position_api(add_position)
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

        # 判断当前公司是否有用工组织架构
        organizations_trees_data = YamlHandle().read_yaml('SingleInterfaceData/Muscat/organizations.yaml')[0]
        organizations_trees_data['employeeid'] = employee_id
        organizations_trees_data['params']['coOrgId'] = company_id
        organizations_trees_res = Muscat(env).organizations(organizations_trees_data)
        data_dict['organizations_trees'] = dict()
        if organizations_trees_res.json()['data'][0]['orgChildren']:
            pass
        else:
            get_organizations_tree_data = dict()
            get_organizations_tree_data['organization_id'] = company_id
            get_organizations_tree_res = OrganizationApi(env).get_organizations_tree_api(get_organizations_tree_data)
            add_department_res = add_department(env, 'WORKFORCE', company_id, '总部',
                                                get_organizations_tree_res.json()['data'][0]['id'])
            data_dict['organizations_trees']['organizationId'] = add_department_res.json()['data']['department_id']
            data_dict['organizations_trees']['organizationName'] = add_department_res.json()['data']['name']
            # data_dict['organizations_trees']['organizationBusinessLevelId'] = add_department_res.json()['data']['organizationBusinessLevelId']
            # data_dict['organizations_trees']['parent_id'] = add_department_res.json()['data']['parent_id']

            # 导入员工
            import_employee_setup = (env, company_id, employee_id)
            TestImportEmployee().test_main_scene(
                YamlHandle().read_yaml('SceneData/ImportEmployeeScene/main_scene.yaml')[0], import_employee_setup)
            # 移动员工至创建的用工部门
            # time.sleep(6)
            get_organization_chart_data = dict()
            get_organization_chart_data['organization_id'] = company_id
            get_organization_chart_res = OrganizationApi(env).get_organization_chart_api(
                get_organization_chart_data)
            employee_ids = []
            for item in get_organization_chart_res.json()['data']['employees']:
                if item['id'] != employee_id:
                    employee_ids.append(item['id'])
            batch_move_employee_data = dict()
            batch_move_employee_data['body'] = dict()
            batch_move_employee_data['body']['to_department_id'] = list()
            batch_move_employee_data['body']['department_id'] = company_id
            batch_move_employee_data['body']['employee_ids'] = employee_ids
            batch_move_employee_data['body']['to_department_id'].append(add_department_res.json()['data']['department_id'])
            EmployeeApi(env).batch_move_employee_api(batch_move_employee_data)
            # 设置部门领导
            set_department_leader = dict()
            set_department_leader['body'] = dict()
            set_department_leader['department_id'] = add_department_res.json()['data']['department_id']
            set_department_leader['body']['header_employee_id'] = employee_ids[0]
            set_department_leader['body']['name'] = add_department_res.json()['data']['name']
            set_department_leader['body']['organizationBusinessLevelId'] = add_department_res.json()['data']['organizationBusinessLevelId']
            set_department_leader['body']['parent_id'] = add_department_res.json()['data']['parent_id']
            DepartmentApi(env).update_department_api(set_department_leader)

        return data_dict

    @pytest.mark.workforce
    @allure.story("用工申请无需审批")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/apply_without_approval.yaml'))
    def test_apply_without_approval(self, data, setup_class):
        with allure.step('第一步：设置用工申请审批流（无需审批）'):
            # 获取用工需求申请审批流列表
            data['get_apply_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_apply_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工申请审批流':
                    workflowSettingId = item['workflowSettingId']
                else:
                    MyLog().error("当前公司没有生成默认审批流")
            # 修改默认审批流为无需审批
            data['update_apply_approval_without_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_apply_approval_without_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_apply_approval_without_approval']['body']['workflowSettingId'] = workflowSettingId
            update_apply_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_apply_approval_without_approval'])
            Assertions().assert_mode(update_apply_approval_res, data['update_apply_approval_without_approval'])

        with allure.step('第二步：发送申请单'):
            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['coOrgId'] = setup_class[
                'company_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['organizationId'] = \
                setup_class['organizations_trees']['organizationId']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 发送用工申请单
            data['send_apply']['body']['applyEmployeeId'] = setup_class['employee_id']
            data['send_apply']['body']['coOrgId'] = setup_class['company_id']
            data['send_apply']['body']['coOrgName'] = setup_class['company_name']
            data['send_apply']['body']['labourCompanyId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['send_apply']['body']['labourCompanyName'] = setup_class['workforce_company_map']['labourCompanyName']
            data['send_apply']['body']['joinDate'] = int(
                time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['probationPeriodExpire'] = int(
                time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['positionId'] = setup_class['position']['positionId']
            data['send_apply']['body']['positionName'] = setup_class['position']['positionName']
            data['send_apply']['body']['projectId'] = setup_class['project']['id']
            data['send_apply']['body']['projectName'] = setup_class['project']['name']
            data['send_apply']['body']['organizationId'] = setup_class['organizations_trees']['organizationId']
            data['send_apply']['body']['organizationName'] = setup_class['organizations_trees']['organizationName']
            data['send_apply']['body']['workflowDeploymentId'] = workflowDeploymentId
            send_apply_res = WorkforceApply(setup_class['env']).send_apply_api(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第三步：获取申请单和需求单'):
            # db中查询刚插入的记录
            database = 'dukang_workforce_dk' + setup_class['env']
            select_sql = "SELECT `code` FROM workforce_application ORDER BY apply_time DESC LIMIT 1"
            code = mysql_operate_select_fetchone(database, select_sql)['code']

            # 获取申请单列表，判断是否有该申请单
            time.sleep(7)
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['code'] == code:
                    application_id = item['applicationId']
                    # Assertions().assert_text(item['workflowStatus'], 'AGREED')
                    break
                else:
                    MyLog().error("申请单列表没有" + code + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = application_id
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_in_text(apply_detail_res.json()['data'],code)
            # 获取需求单列表，
            data['get_require_list']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            get_require_list_res = WorkforceTicket(setup_class['env']).get_require_list_api(data['get_require_list'])
            allure.attach(str(data['get_require_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_require_list_res, data['get_require_list'])
            for item in get_require_list_res.json()['data']:
                if item['applicationCode'] == code:
                    require_id = item['id']
                    # Assertions().assert_text(item['status'], 'PENDING')
                    break
                MyLog().error("需求单没有" + code + "需求记录")
            # 查看需求单详情
            data['get_require_detail']['id'] = require_id
            require_detail_res = WorkforceTicket(setup_class['env']).get_require_detail_api(data['get_require_detail'])
            allure.attach(str(data['get_require_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(require_detail_res.text, "get_require_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(require_detail_res, data['get_require_detail'])
            Assertions().assert_in_text(require_detail_res.json()['data'], code)
        return application_id, require_id, code

    @pytest.mark.workforce
    @allure.story("用工申请自动审批")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/apply_automatic_approval.yaml'))
    def test_apply_automatic_approval(self, data, setup_class):

        with allure.step('第一步：设置用工申请审批流（自动审批）'):
            # 获取用工需求申请审批流列表
            data['get_apply_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_apply_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工申请审批流':
                    workflowSettingId = item['workflowSettingId']
                else:
                    MyLog().error("当前公司没有生成默认审批流")
            # 修改默认审批流为自动审批
            data['update_apply_approval_automatic_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_apply_approval_automatic_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_apply_approval_automatic_approval']['body']['workflowSettingId'] = workflowSettingId
            data['update_apply_approval_automatic_approval']['body']['workflowSettingRuleGroupDtoList'][0][
                'workflowSettingApproverList'][0]['employeeId'] = setup_class['employee_id']
            update_apply_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_apply_approval_automatic_approval'])
            Assertions().assert_mode(update_apply_approval_res, data['update_apply_approval_automatic_approval'])

        with allure.step('第二步：发送申请单'):
            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['coOrgId'] = setup_class[
                'company_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['organizationId'] = \
                setup_class['organizations_trees']['organizationId']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 发送用工申请单
            data['send_apply']['body']['applyEmployeeId'] = setup_class['employee_id']
            data['send_apply']['body']['coOrgId'] = setup_class['company_id']
            data['send_apply']['body']['coOrgName'] = setup_class['company_name']
            data['send_apply']['body']['labourCompanyId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['send_apply']['body']['labourCompanyName'] = setup_class['workforce_company_map']['labourCompanyName']
            data['send_apply']['body']['joinDate'] = int(
                time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['probationPeriodExpire'] = int(
                time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['positionId'] = setup_class['position']['positionId']
            data['send_apply']['body']['positionName'] = setup_class['position']['positionName']
            data['send_apply']['body']['projectId'] = setup_class['project']['id']
            data['send_apply']['body']['projectName'] = setup_class['project']['name']
            data['send_apply']['body']['organizationId'] = setup_class['organizations_trees']['organizationId']
            data['send_apply']['body']['organizationName'] = setup_class['organizations_trees']['organizationName']
            data['send_apply']['body']['workflowDeploymentId'] = workflowDeploymentId
            approverList = get_approval_by_organization_res.json()['data']['employeeVoList'][1]
            approverList['employeeId'] = setup_class['employee_id']
            data['send_apply']['body']['approverList'].append(approverList)
            send_apply_res = WorkforceApply(setup_class['env']).send_apply_api(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第三步：获取申请单和需求单'):
            # db中查询刚插入的记录
            database = 'dukang_workforce_dk' + setup_class['env']
            select_sql = "SELECT `code` FROM workforce_application ORDER BY apply_time DESC LIMIT 1"
            code = mysql_operate_select_fetchone(database, select_sql)['code']

            # 获取申请单列表，判断是否有该申请单
            time.sleep(7)
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['code'] == code:
                    application_id = item['applicationId']
                    # Assertions().assert_text(item['workflowStatus'], 'AGREED')
                    break
                else:
                    MyLog().error("申请单列表没有" + code + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = application_id
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_in_text(apply_detail_res.json()['data'], code)
            # 获取需求单列表
            data['get_require_list']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            get_require_list_res = WorkforceTicket(setup_class['env']).get_require_list_api(data['get_require_list'])
            allure.attach(str(data['get_require_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_require_list_res, data['get_require_list'])
            for item in get_require_list_res.json()['data']:
                if item['applicationCode'] == code:
                    require_id = item['id']
                    # Assertions().assert_text(item['status'], 'PENDING')
                    break
                MyLog().error("需求单没有" + code + "需求记录")
            # 查看需求单详情
            data['get_require_detail']['id'] = require_id
            require_detail_res = WorkforceTicket(setup_class['env']).get_require_detail_api(
                data['get_require_detail'])
            allure.attach(str(data['get_require_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(require_detail_res.text, "get_require_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(require_detail_res, data['get_require_detail'])
            Assertions().assert_in_text(require_detail_res.json()['data'], code)
        return application_id, require_id, code

    @pytest.mark.workforce
    @allure.story("用工申请通过（需要审批）")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/agree_apply_approval.yaml'))
    def test_agree_apply_approval(self, data, setup_class):

        with allure.step('第一步：设置用工申请审批流(需要上级领导审批)'):
            # 获取用工需求申请审批流列表
            data['get_apply_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_apply_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工申请审批流':
                    workflowSettingId = item['workflowSettingId']
                else:
                    MyLog().error("当前公司没有生成默认审批流")
            # 修改默认审批流为需要上级领导审批
            data['update_apply_approval_need_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_apply_approval_need_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_apply_approval_need_approval']['body']['workflowSettingId'] = workflowSettingId
            data['update_apply_approval_need_approval']['body']['workflowSettingRuleGroupDtoList'][0][
                'workflowSettingApproverList'][0]['employeeId'] = setup_class['employee_id']
            update_apply_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_apply_approval_need_approval'])
            Assertions().assert_mode(update_apply_approval_res, data['update_apply_approval_need_approval'])

        with allure.step('第二步：发送申请单'):

            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['coOrgId'] = setup_class[
                'company_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['organizationId'] = \
                setup_class['organizations_trees']['organizationId']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 发送用工申请单
            data['send_apply']['body']['applyEmployeeId'] = setup_class['employee_id']
            data['send_apply']['body']['coOrgId'] = setup_class['company_id']
            data['send_apply']['body']['coOrgName'] = setup_class['company_name']
            data['send_apply']['body']['labourCompanyId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['send_apply']['body']['labourCompanyName'] = setup_class['workforce_company_map']['labourCompanyName']
            data['send_apply']['body']['joinDate'] = int(
                time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['probationPeriodExpire'] = int(
                time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['positionId'] = setup_class['position']['positionId']
            data['send_apply']['body']['positionName'] = setup_class['position']['positionName']
            data['send_apply']['body']['projectId'] = setup_class['project']['id']
            data['send_apply']['body']['projectName'] = setup_class['project']['name']
            data['send_apply']['body']['organizationId'] = setup_class['organizations_trees']['organizationId']
            data['send_apply']['body']['organizationName'] = setup_class['organizations_trees']['organizationName']
            data['send_apply']['body']['workflowDeploymentId'] = workflowDeploymentId
            approverList = get_approval_by_organization_res.json()['data']['employeeVoList'][1]
            approverList['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            data['send_apply']['body']['approverList'].append(approverList)
            send_apply_res = WorkforceApply(setup_class['env']).send_apply_api(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第三步：获取申请单'):
            # db中查询刚插入的记录
            database = 'dukang_workforce_dk' + setup_class['env']
            select_sql = "SELECT `code` FROM workforce_application ORDER BY apply_time DESC LIMIT 1"
            code = mysql_operate_select_fetchone(database, select_sql)['code']

            # 获取申请单列表，判断是否有该申请单
            # time.sleep(7)
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['code'] == code:
                    application_id = item['applicationId']
                    Assertions().assert_text(item['workflowStatus'], 'PENDING')
                    break
                else:
                    MyLog().error("申请单列表没有" + code + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = application_id
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_in_text(apply_detail_res.json()['data'], code)

        with allure.step('第四步：审批通过'):
            # 获取审批人待审批列表
            data['get_application_await_list']['body']['coOrgId'] = setup_class['company_id']
            data['get_application_await_list']['body']['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            get_application_await_list_res = WorkforceWorkflow(setup_class['env']).workflow_application_await_list_api(data['get_application_await_list'])
            Assertions().assert_mode(get_application_await_list_res, data['get_application_await_list'])
            Assertions().assert_in_text(get_application_await_list_res.json()['data'], application_id)
            # 审批通过
            data['agree_apply_approvel']['body']['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            data['agree_apply_approvel']['body']['formId'] = application_id
            data['agree_apply_approvel']['body']['formWorkflowId'] = apply_detail_res.json()['data']['formWorkflowId']
            data['agree_apply_approvel']['body']['processInstanceId'] = apply_detail_res.json()['data']['processInstanceId']
            workflow_node_approve_res = WorkflowDomain(setup_class['env']).workflow_node_approve_api(data['agree_apply_approvel'])
            Assertions().assert_mode(workflow_node_approve_res, data['agree_apply_approvel'])

        with allure.step('第五步：查看申请单和需求单'):
            time.sleep(7)
            # 获取申请单列表，判断是否有该申请单
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['applicationId'] == application_id:
                    Assertions().assert_text(item['workflowStatus'], 'AGREED')
                    break
                else:
                    MyLog().error("申请单列表没有" + code + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = application_id
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_text(apply_detail_res.json()['data']['workflowStatus'], "AGREED")
            # 获取需求单列表
            data['get_require_list']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            get_require_list_res = WorkforceTicket(setup_class['env']).get_require_list_api(data['get_require_list'])
            allure.attach(str(data['get_require_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_require_list_res, data['get_require_list'])
            for item in get_require_list_res.json()['data']:
                if item['applicationCode'] == code:
                    require_id = item['id']
                    Assertions().assert_text(item['status'], 'PENDING')
                    break
                else:
                    MyLog().error("需求单没有" + code + "需求记录")
            # 查看需求单详情
            data['get_require_detail']['id'] = require_id
            require_detail_res = WorkforceTicket(setup_class['env']).get_require_detail_api(
                data['get_require_detail'])
            allure.attach(str(data['get_require_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(require_detail_res.text, "get_require_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(require_detail_res, data['get_require_detail'])
            Assertions().assert_text(require_detail_res.json()['data']['status'], 'PENDING')
        return application_id, require_id, code

    @pytest.mark.workforce
    @allure.story("用工申请拒绝(需要审批)")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/refuse_apply_approve.yaml'))
    def test_refuse_apply_approval(self, data, setup_class):

        with allure.step('第一步：设置用工申请审批流(需要上级领导审批)'):
            # 获取用工需求申请审批流列表
            data['get_apply_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_apply_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工申请审批流':
                    workflowSettingId = item['workflowSettingId']
                else:
                    MyLog().error("当前公司没有生成默认审批流")
            # 修改默认审批流为需要上级领导审批
            data['update_apply_approval_need_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_apply_approval_need_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_apply_approval_need_approval']['body']['workflowSettingId'] = workflowSettingId
            data['update_apply_approval_need_approval']['body']['workflowSettingRuleGroupDtoList'][0][
                'workflowSettingApproverList'][0]['employeeId'] = setup_class['employee_id']
            update_apply_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_apply_approval_need_approval'])
            Assertions().assert_mode(update_apply_approval_res, data['update_apply_approval_need_approval'])

        with allure.step('第二步：发送申请单'):

            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['coOrgId'] = setup_class[
                'company_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['organizationId'] = \
                setup_class['organizations_trees']['organizationId']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 发送用工申请单
            data['send_apply']['body']['applyEmployeeId'] = setup_class['employee_id']
            data['send_apply']['body']['coOrgId'] = setup_class['company_id']
            data['send_apply']['body']['coOrgName'] = setup_class['company_name']
            data['send_apply']['body']['labourCompanyId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['send_apply']['body']['labourCompanyName'] = setup_class['workforce_company_map']['labourCompanyName']
            data['send_apply']['body']['joinDate'] = int(
                time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['probationPeriodExpire'] = int(
                time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['positionId'] = setup_class['position']['positionId']
            data['send_apply']['body']['positionName'] = setup_class['position']['positionName']
            data['send_apply']['body']['projectId'] = setup_class['project']['id']
            data['send_apply']['body']['projectName'] = setup_class['project']['name']
            data['send_apply']['body']['organizationId'] = setup_class['organizations_trees']['organizationId']
            data['send_apply']['body']['organizationName'] = setup_class['organizations_trees']['organizationName']
            data['send_apply']['body']['workflowDeploymentId'] = workflowDeploymentId
            approverList = get_approval_by_organization_res.json()['data']['employeeVoList'][1]
            approverList['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            data['send_apply']['body']['approverList'].append(approverList)
            send_apply_res = WorkforceApply(setup_class['env']).send_apply_api(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第三步：获取申请单'):
            # db中查询刚插入的记录
            database = 'dukang_workforce_dk' + setup_class['env']
            select_sql = "SELECT `code` FROM workforce_application ORDER BY apply_time DESC LIMIT 1"
            code = mysql_operate_select_fetchone(database, select_sql)['code']

            # 获取申请单列表，判断是否有该申请单
            # time.sleep(7)
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['code'] == code:
                    application_id = item['applicationId']
                    Assertions().assert_text(item['workflowStatus'], 'PENDING')
                    break
                else:
                    MyLog().error("申请单列表没有" + code + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = application_id
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_in_text(apply_detail_res.json()['data'], code)

        with allure.step('第四步：审批拒绝'):
            # 获取审批人待审批列表
            data['get_application_await_list']['body']['coOrgId'] = setup_class['company_id']
            data['get_application_await_list']['body']['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            get_application_await_list_res = WorkforceWorkflow(setup_class['env']).workflow_application_await_list_api(data['get_application_await_list'])
            Assertions().assert_mode(get_application_await_list_res, data['get_application_await_list'])
            Assertions().assert_in_text(get_application_await_list_res.json()['data'], application_id)
            # 审批拒绝
            data['agree_apply_approvel']['body']['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            data['agree_apply_approvel']['body']['formId'] = application_id
            data['agree_apply_approvel']['body']['formWorkflowId'] = apply_detail_res.json()['data']['formWorkflowId']
            data['agree_apply_approvel']['body']['processInstanceId'] = apply_detail_res.json()['data']['processInstanceId']
            workflow_node_approve_res = WorkflowDomain(setup_class['env']).workflow_node_approve_api(data['agree_apply_approvel'])
            Assertions().assert_mode(workflow_node_approve_res, data['agree_apply_approvel'])

        with allure.step('第五步：查看申请单'):
            time.sleep(7)
            # 获取申请单列表，判断是否有该申请单
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['applicationId'] == application_id:
                    Assertions().assert_text(item['workflowStatus'], 'REFUSED')
                    break
                else:
                    MyLog().error("申请单列表没有" + code + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = application_id
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_text(apply_detail_res.json()['data']['workflowStatus'], "REFUSED")

    @pytest.mark.workforce
    @allure.story("撤销申请")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/withdraw_apply.yaml'))
    def test_withdraw_apply(self, data, setup_class):

        with allure.step('第一步：设置用工申请审批流(需要上级领导审批)'):
            # 获取用工需求申请审批流列表
            data['get_apply_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_apply_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工申请审批流':
                    workflowSettingId = item['workflowSettingId']
                else:
                    MyLog().error("当前公司没有生成默认审批流")
            # 修改默认审批流为需要上级领导审批
            data['update_apply_approval_need_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_apply_approval_need_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_apply_approval_need_approval']['body']['workflowSettingId'] = workflowSettingId
            data['update_apply_approval_need_approval']['body']['workflowSettingRuleGroupDtoList'][0][
                'workflowSettingApproverList'][0]['employeeId'] = setup_class['employee_id']
            update_apply_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_apply_approval_need_approval'])
            Assertions().assert_mode(update_apply_approval_res, data['update_apply_approval_need_approval'])

        with allure.step('第二步：发送申请单'):

            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['coOrgId'] = setup_class[
                'company_id']
            data['get_approval_by_organization']['body']['workforceApplicationDto']['organizationId'] = \
                setup_class['organizations_trees']['organizationId']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 发送用工申请单
            data['send_apply']['body']['applyEmployeeId'] = setup_class['employee_id']
            data['send_apply']['body']['coOrgId'] = setup_class['company_id']
            data['send_apply']['body']['coOrgName'] = setup_class['company_name']
            data['send_apply']['body']['labourCompanyId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['send_apply']['body']['labourCompanyName'] = setup_class['workforce_company_map']['labourCompanyName']
            data['send_apply']['body']['joinDate'] = int(
                time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['probationPeriodExpire'] = int(
                time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            data['send_apply']['body']['positionId'] = setup_class['position']['positionId']
            data['send_apply']['body']['positionName'] = setup_class['position']['positionName']
            data['send_apply']['body']['projectId'] = setup_class['project']['id']
            data['send_apply']['body']['projectName'] = setup_class['project']['name']
            data['send_apply']['body']['organizationId'] = setup_class['organizations_trees']['organizationId']
            data['send_apply']['body']['organizationName'] = setup_class['organizations_trees']['organizationName']
            data['send_apply']['body']['workflowDeploymentId'] = workflowDeploymentId
            approverList = get_approval_by_organization_res.json()['data']['employeeVoList'][1]
            approverList['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            data['send_apply']['body']['approverList'].append(approverList)
            send_apply_res = WorkforceApply(setup_class['env']).send_apply_api(data['send_apply'])
            allure.attach(str(data['send_apply']), "请求数据", allure.attachment_type.JSON)
            allure.attach(send_apply_res.text, "send_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(send_apply_res, data['send_apply'])

        with allure.step('第三步：获取申请单'):
            # db中查询刚插入的记录
            database = 'dukang_workforce_dk' + setup_class['env']
            select_sql = "SELECT `code` FROM workforce_application ORDER BY apply_time DESC LIMIT 1"
            code = mysql_operate_select_fetchone(database, select_sql)['code']

            # 获取申请单列表，判断是否有该申请单
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['code'] == code:
                    application_id = item['applicationId']
                    Assertions().assert_text(item['workflowStatus'], 'PENDING')
                    break
                else:
                    MyLog().error("申请单列表没有" + code + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = application_id
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_in_text(apply_detail_res.json()['data'], code)

        with allure.step('第四步：撤销当前申请单'):
            data['withdraw_apply']['application_id'] = application_id
            data['withdraw_apply']['body']['form_workflow_id'] = apply_detail_res.json()['data']['formWorkflowId']
            data['withdraw_apply']['body']['process_instance_id'] = apply_detail_res.json()['data']['processInstanceId']
            withdraw_apply_res = WorkforceApply(setup_class['env']).withdraw_apply_api(data['withdraw_apply'])
            allure.attach(str(data['withdraw_apply']), "请求数据", allure.attachment_type.JSON)
            allure.attach(withdraw_apply_res.text, "withdraw_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(withdraw_apply_res, data['withdraw_apply'])

        with allure.step('第五步：获取申请列表,判断当前申请单状态是否变更为已撤销'):
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            for item in apply_list_res.json()['data']:
                if item['code'] == code:
                    Assertions().assert_text(item['workflowStatus'], 'ROLLBACK')
                    break
                else:
                    MyLog().error("撤销申请单之后在对应申请单列表没有找到该订单")

    @pytest.mark.workforce
    @allure.story("停止申请")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/stop_apply.yaml'))
    def test_stop_apply(self, data, setup_class):
        test_agree_apply_approval_result = self.test_agree_apply_approval(YamlHandle().read_yaml('SceneData/WorkforceScene/agree_apply_approval.yaml')[0], setup_class)

        with allure.step('第一步：停止用工申请'):
            data['stop_apply']['application_id'] = test_agree_apply_approval_result[0]
            allure.attach(str(data['stop_apply']), "请求数据", allure.attachment_type.JSON)
            stop_apply_res = WorkforceApply(setup_class['env']).stop_apply_api(data['stop_apply'])
            allure.attach(stop_apply_res.text, "stop_apply_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(stop_apply_res, data['stop_apply'])

        with allure.step('第二步：获取申请单和需求单'):
            # 获取申请单列表，判断是否有该申请单
            data['get_apply_list']['body']['coOrgId'] = setup_class['company_id']
            get_apply_list_res = WorkforceApply(setup_class['env']).apply_list_api(data['get_apply_list'])
            allure.attach(str(data['get_apply_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_apply_list_res.text, "apply_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_apply_list_res, data['get_apply_list'])
            for item in get_apply_list_res.json()['data']:
                if item['applicationId'] == test_agree_apply_approval_result[0]:
                    Assertions().assert_text(item['workflowStatus'], 'STOP')
                    break
                else:
                    MyLog().error("申请单列表没有" + test_agree_apply_approval_result[2] + "申请记录")
            # 查看申请单详情页
            data['apply_detail']['application_id'] = test_agree_apply_approval_result[0]
            apply_detail_res = WorkforceApply(setup_class['env']).apply_detail_api(data['apply_detail'])
            allure.attach(str(data['apply_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(apply_detail_res.text, "apply_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(apply_detail_res, data['apply_detail'])
            Assertions().assert_text(apply_detail_res.json()['data']['workflowStatus'], "STOP")
            # 获取需求单列表
            data['get_require_list']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            get_require_list_res = WorkforceTicket(setup_class['env']).get_require_list_api(data['get_require_list'])
            allure.attach(str(data['get_require_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_require_list_res.text, "require_list_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(get_require_list_res, data['get_require_list'])
            for item in get_require_list_res.json()['data']:
                if item['applicationCode'] == test_agree_apply_approval_result[2]:
                    Assertions().assert_text(item['status'], 'STOP')
                    break
                else:
                    MyLog().error("需求单没有" + test_agree_apply_approval_result[2] + "需求记录")
            # 查看需求单详情
            data['get_require_detail']['id'] = test_agree_apply_approval_result[1]
            require_detail_res = WorkforceTicket(setup_class['env']).get_require_detail_api(
                data['get_require_detail'])
            allure.attach(str(data['get_require_detail']), "请求数据", allure.attachment_type.JSON)
            allure.attach(require_detail_res.text, "get_require_detail_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(require_detail_res, data['get_require_detail'])
            Assertions().assert_text(require_detail_res.json()['data']['status'], 'STOP')

    @pytest.mark.workforce
    @allure.story("拒绝接收")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/refuse_receive.yaml'))
    def test_refuse_receive(self, data, setup_class):
        test_apply_automatic_approval_result = self.test_apply_automatic_approval(YamlHandle().read_yaml('SceneData/WorkforceScene/apply_automatic_approval.yaml')[0], setup_class)

        with allure.step('第一步：获取关联申请,判断是否存在生成的需求单'):
            data['relevance_apply']['params']['coOrgId'] = setup_class['company_id']
            relevance_apply_res = WorkforceDispatch(setup_class['env']).relevance_apply_api(data['relevance_apply'])
            for item in relevance_apply_res.json()['data']:
                if item['code'] == test_apply_automatic_approval_result[2]:
                    begin_time = item['beginTime']
                    end_time = item['endTime']
                    ticket_id = item['ticketId']
                    break

        with allure.step('第二步：根据需求时间查询空闲员工'):
            data['free_employee']['body']['beginTime'] = begin_time
            data['free_employee']['body']['endTime'] = end_time
            data['free_employee']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            workforce_employees_free_res = WorkforceEmployeeDomain(setup_class['env']).workforce_employees_free(
                data['free_employee'])
            Assertions().assert_mode(workforce_employees_free_res, data['free_employee'])
            employee_infomation = workforce_employees_free_res.json()['data'][1]

        with allure.step('第三步：乙方根据需求单派遣一个员工'):
            data['dispatch']['body']['beginTime'] = begin_time
            data['dispatch']['body']['endTime'] = end_time
            data['dispatch']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['dispatch']['body']['dispatchCoOrgId'] = setup_class['company_id']
            data['dispatch']['body']['workforceRequestId'] = ticket_id
            data['dispatch']['body']['employeeIds'].append(employee_infomation['id'])
            workforceDispatchEmployeeBasisDtos = dict()
            workforceDispatchEmployeeBasisDtos['address'] = employee_infomation['address']
            workforceDispatchEmployeeBasisDtos['birthday'] = employee_infomation['birthDateLong']
            workforceDispatchEmployeeBasisDtos['coOrgId'] = employee_infomation['coOrgId']
            workforceDispatchEmployeeBasisDtos['displayName'] = employee_infomation['displayName']
            workforceDispatchEmployeeBasisDtos['employeeId'] = employee_infomation['id']
            workforceDispatchEmployeeBasisDtos['idCard'] = employee_infomation['identitys'][0]['number']
            workforceDispatchEmployeeBasisDtos['mobile'] = employee_infomation['mobile']
            workforceDispatchEmployeeBasisDtos['mobileAreaCode'] = employee_infomation['mobileArea']
            workforceDispatchEmployeeBasisDtos['sex'] = employee_infomation['genderValue']
            workforceDispatchEmployeeBasisDtos['workforceEmployeeCode'] = employee_infomation['employee_code']
            if employee_infomation['employeeContactVos']:
                workforceDispatchEmployeeBasisDtos['emergencyMobile'] = employee_infomation['employeeContactVos'][0]['mobile']
                workforceDispatchEmployeeBasisDtos['emergencyMobileAreaCode'] = employee_infomation['employeeContactVos'][0]['mobileAreaCode']
                workforceDispatchEmployeeBasisDtos['emergencyName'] = employee_infomation['employeeContactVos'][0]['name']
                workforceDispatchEmployeeBasisDtos['emergencyRelationshipValue'] = employee_infomation['employeeContactVos'][0]['relationshipValue']
            data['dispatch']['body']['workforceDispatchEmployeeBasisDtos'].append(workforceDispatchEmployeeBasisDtos)
            dispatch_res = WorkforceDispatch(setup_class['env']).dispatch_api(data['dispatch'])
            allure.attach(str(data['dispatch']), "请求数据", allure.attachment_type.JSON)
            allure.attach(dispatch_res.text, "dispatch_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(dispatch_res, data['dispatch'])

        with allure.step('第四步：获取指派单和接收单'):
            database = 'dukang_workforce_dk' + setup_class['env']
            dispatch_id_sql = "SELECT id FROM workforce_working_assign where type='DISPATCH' ORDER BY dispatch_time DESC LIMIT 1"
            dispatch_id = mysql_operate_select_fetchone(database, dispatch_id_sql)['id']
            receive_id_sql = "SELECT id FROM workforce_working_assign where type='RECEIVE' ORDER BY dispatch_time DESC LIMIT 1"
            receive_id = mysql_operate_select_fetchone(database,receive_id_sql)['id']
            data['dispatch_list']['params']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            dispatch_list_res = WorkforceDispatch(setup_class['env']).dispatch_list_api(data['dispatch_list'])
            allure.attach(str(data['dispatch_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(dispatch_list_res.text, "dispatch_list_api返回结果", allure.attachment_type.JSON)
            for item in dispatch_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == dispatch_id:
                    Assertions().assert_text(item['status'], "DISPOSE")
                    break
                MyLog().error("没有找到该派遣单单")
            data['recevice_list']['params']['coOrgId'] = setup_class['company_id']
            recevice_list_res = WorkforceRecevice(setup_class['env']).recevice_list_api(data['recevice_list'])
            allure.attach(str(data['recevice_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(recevice_list_res.text, "recevice_list_api返回结果", allure.attachment_type.JSON)
            for item in recevice_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == receive_id:
                    Assertions().assert_text(item['status'], "DISPOSE")
                    break
                MyLog().error("没有找到该接收单")

        with allure.step('第五步：拒绝派遣过来的人员'):
            data['refuse_receive']['body']['beginTime'] = begin_time
            data['refuse_receive']['body']['endTime'] = end_time
            data['refuse_receive']['body']['coOrgId'] = setup_class['company_id']
            data['refuse_receive']['body']['ticketId'] = ticket_id
            data['refuse_receive']['body']['workforceWorkingAssignId'] = receive_id
            employeeCompanyDtos = dict()
            employeeCompanyDtos['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            employeeCompanyDtos['employeeId'] = employee_infomation['id']
            data['refuse_receive']['body']['employeeCompanyDtos'].append(employeeCompanyDtos)
            refuse_recevice_res = WorkforceRecevice(setup_class['env']).refuse_recevice_api(data['refuse_receive'])
            Assertions().assert_mode(refuse_recevice_res, data['refuse_receive'])

        with allure.step('第六步：获取指派单和接收单状态'):
            data['dispatch_list']['params']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            dispatch_list_res = WorkforceDispatch(setup_class['env']).dispatch_list_api(data['dispatch_list'])
            for item in dispatch_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == dispatch_id:
                    Assertions().assert_text(item['status'], "REFUSE")
                    break
                MyLog().error("没有找到该派遣单单")
            data['recevice_list']['params']['coOrgId'] = setup_class['company_id']
            recevice_list_res = WorkforceRecevice(setup_class['env']).recevice_list_api(data['recevice_list'])
            for item in recevice_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == receive_id:
                    Assertions().assert_text(item['status'], "REFUSE")
                    break
                MyLog().error("没有找到该接收单")

    @pytest.mark.workforce
    @allure.story("同意接收")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/agree_receive.yaml'))
    def test_agree_receive(self, data, setup_class):
        test_apply_automatic_approval_result = self.test_apply_automatic_approval(
            YamlHandle().read_yaml('SceneData/WorkforceScene/apply_automatic_approval.yaml')[0], setup_class)
        application_id = test_apply_automatic_approval_result[0]
        require_id = test_apply_automatic_approval_result[1]
        code = test_apply_automatic_approval_result[2]

        with allure.step('第一步：获取关联申请,判断是否存在生成的需求单'):
            data['relevance_apply']['params']['coOrgId'] = setup_class['company_id']
            relevance_apply_res = WorkforceDispatch(setup_class['env']).relevance_apply_api(data['relevance_apply'])
            for item in relevance_apply_res.json()['data']:
                if item['code'] == code:
                    begin_time = item['beginTime']
                    end_time = item['endTime']
                    ticket_id = item['ticketId']
                    break

        with allure.step('第二步：根据需求时间查询空闲员工'):
            data['free_employee']['body']['beginTime'] = begin_time
            data['free_employee']['body']['endTime'] = end_time
            data['free_employee']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            workforce_employees_free_res = WorkforceEmployeeDomain(setup_class['env']).workforce_employees_free(
                data['free_employee'])
            Assertions().assert_mode(workforce_employees_free_res, data['free_employee'])
            employee_infomation = workforce_employees_free_res.json()['data'][1]

        with allure.step('第三步：乙方根据需求单派遣一个员工'):
            data['dispatch']['body']['beginTime'] = begin_time
            data['dispatch']['body']['endTime'] = end_time
            data['dispatch']['body']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            data['dispatch']['body']['dispatchCoOrgId'] = setup_class['company_id']
            data['dispatch']['body']['workforceRequestId'] = ticket_id
            data['dispatch']['body']['employeeIds'].append(employee_infomation['id'])
            workforceDispatchEmployeeBasisDtos = dict()
            workforceDispatchEmployeeBasisDtos['address'] = employee_infomation['address']
            workforceDispatchEmployeeBasisDtos['birthday'] = employee_infomation['birthDateLong']
            workforceDispatchEmployeeBasisDtos['coOrgId'] = employee_infomation['coOrgId']
            workforceDispatchEmployeeBasisDtos['displayName'] = employee_infomation['displayName']
            workforceDispatchEmployeeBasisDtos['employeeId'] = employee_infomation['id']
            workforceDispatchEmployeeBasisDtos['idCard'] = employee_infomation['identitys'][0]['number']
            workforceDispatchEmployeeBasisDtos['mobile'] = employee_infomation['mobile']
            workforceDispatchEmployeeBasisDtos['mobileAreaCode'] = employee_infomation['mobileArea']
            workforceDispatchEmployeeBasisDtos['sex'] = employee_infomation['genderValue']
            workforceDispatchEmployeeBasisDtos['workforceEmployeeCode'] = employee_infomation['employee_code']
            if employee_infomation['employeeContactVos']:
                workforceDispatchEmployeeBasisDtos['emergencyMobile'] = employee_infomation['employeeContactVos'][0][
                    'mobile']
                workforceDispatchEmployeeBasisDtos['emergencyMobileAreaCode'] = \
                employee_infomation['employeeContactVos'][0]['mobileAreaCode']
                workforceDispatchEmployeeBasisDtos['emergencyName'] = employee_infomation['employeeContactVos'][0][
                    'name']
                workforceDispatchEmployeeBasisDtos['emergencyRelationshipValue'] = \
                employee_infomation['employeeContactVos'][0]['relationshipValue']
            data['dispatch']['body']['workforceDispatchEmployeeBasisDtos'].append(workforceDispatchEmployeeBasisDtos)
            dispatch_res = WorkforceDispatch(setup_class['env']).dispatch_api(data['dispatch'])
            allure.attach(str(data['dispatch']), "请求数据", allure.attachment_type.JSON)
            allure.attach(dispatch_res.text, "dispatch_api返回结果", allure.attachment_type.JSON)
            Assertions().assert_mode(dispatch_res, data['dispatch'])

        with allure.step('第四步：获取指派单和接收单'):
            database = 'dukang_workforce_dk' + setup_class['env']
            dispatch_id_sql = "SELECT id FROM workforce_working_assign where type='DISPATCH' ORDER BY dispatch_time DESC LIMIT 1"
            dispatch_id = mysql_operate_select_fetchone(database, dispatch_id_sql)['id']
            receive_id_sql = "SELECT id FROM workforce_working_assign where type='RECEIVE' ORDER BY dispatch_time DESC LIMIT 1"
            receive_id = mysql_operate_select_fetchone(database, receive_id_sql)['id']
            data['dispatch_list']['params']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            dispatch_list_res = WorkforceDispatch(setup_class['env']).dispatch_list_api(data['dispatch_list'])
            allure.attach(str(data['dispatch_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(dispatch_list_res.text, "dispatch_list_api返回结果", allure.attachment_type.JSON)
            for item in dispatch_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == dispatch_id:
                    Assertions().assert_text(item['status'], "DISPOSE")
                    break
                MyLog().error("没有找到该派遣单单")
            data['recevice_list']['params']['coOrgId'] = setup_class['company_id']
            recevice_list_res = WorkforceRecevice(setup_class['env']).recevice_list_api(data['recevice_list'])
            allure.attach(str(data['recevice_list']), "请求数据", allure.attachment_type.JSON)
            allure.attach(recevice_list_res.text, "recevice_list_api返回结果", allure.attachment_type.JSON)
            for item in recevice_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == receive_id:
                    Assertions().assert_text(item['status'], "DISPOSE")
                    break
                MyLog().error("没有找到该接收单")

        with allure.step('第五步：同意派遣过来的人员'):
            data['agree_receive']['body']['beginTime'] = begin_time
            data['agree_receive']['body']['endTime'] = end_time
            data['agree_receive']['body']['coOrgId'] = setup_class['company_id']
            data['agree_receive']['body']['ticketId'] = ticket_id
            data['agree_receive']['body']['workforceWorkingAssignId'] = receive_id
            employeeCompanyDtos = dict()
            employeeCompanyDtos['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            employeeCompanyDtos['employeeId'] = employee_infomation['id']
            data['agree_receive']['body']['employeeCompanyDtos'].append(employeeCompanyDtos)
            refuse_recevice_res = WorkforceRecevice(setup_class['env']).agree_recevice_api(data['agree_receive'])
            Assertions().assert_mode(refuse_recevice_res, data['agree_receive'])

        with allure.step('第六步：获取指派单和接收单状态'):
            data['dispatch_list']['params']['coOrgId'] = setup_class['workforce_company_map']['labourCompanyId']
            dispatch_list_res = WorkforceDispatch(setup_class['env']).dispatch_list_api(data['dispatch_list'])
            for item in dispatch_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == dispatch_id:
                    Assertions().assert_text(item['status'], "RECEIVE")
                    break
                MyLog().error("没有找到该派遣单单")
            data['recevice_list']['params']['coOrgId'] = setup_class['company_id']
            recevice_list_res = WorkforceRecevice(setup_class['env']).recevice_list_api(data['recevice_list'])
            for item in recevice_list_res.json()['data']:
                if item['workforceWorkingAssignId'] == receive_id:
                    Assertions().assert_text(item['status'], "RECEIVE")
                    break
                MyLog().error("没有找到该接收单")
        return employee_infomation['id']

    @pytest.mark.workforce
    @allure.story("用工登记自动审批")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/register_automatic_approval.yaml'))
    def test_register_automatic_approval(self, data, setup_class):
        test_agree_receive_result = self.test_agree_receive(YamlHandle().read_yaml('SceneData/WorkforceScene/agree_receive.yaml')[0], setup_class)
        dispatch_employee_id = test_agree_receive_result

        with allure.step('第一步：设置用工登记审批流（自动审批）'):
            # 获取用工登记审批流列表
            data['get_register_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_register_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工登记审批流':
                    workflowSettingId = item['workflowSettingId']
                MyLog().error("当前公司没有生成默认登记审批流")

            # 修改默认审批流为自动审批
            data['update_register_approval_automatic_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_register_approval_automatic_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_register_approval_automatic_approval']['body']['workflowSettingId'] = workflowSettingId
            data['update_register_approval_automatic_approval']['body']['workflowSettingRuleGroupDtoList'][0][
                'workflowSettingApproverList'][0]['employeeId'] = setup_class['employee_id']
            update_register_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_register_approval_automatic_approval'])
            Assertions().assert_mode(update_register_approval_res, data['update_register_approval_automatic_approval'])

        with allure.step('第二步：登记派遣过来的员工'):
            # 获取登记列表
            data['get_register_list']['body']['coOrgId'] = setup_class['company_id']
            get_register_list_res = WorkforceRegister(setup_class['env']).get_register_list_api(data['get_register_list'])
            Assertions().assert_mode(get_register_list_res, data['get_register_list'])
            for item in get_register_list_res.json()['data']:
                if item['employeeId'] == dispatch_employee_id:
                    workforceApplicationId = item['workforceApplicationId']
                    workforceAssignRelationId = item['workforceAssignRelationId']
                MyLog().error('登记列表没有找到' + str(dispatch_employee_id) + '员工')

            # 获取登记详情
            data['get_register_detail']['params']['employeeId'] = dispatch_employee_id
            data['get_register_detail']['params']['workforceApplicationId'] = workforceApplicationId
            data['get_register_detail']['params']['workforceAssignRelationId'] = workforceAssignRelationId
            get_register_detail_res = WorkforceRegister(setup_class['env']).get_register_detail_api(data['get_register_detail'])
            Assertions().assert_mode(get_register_detail_res, data['get_register_detail'])

            # 获取部门信息
            data['get_department']['department_id'] = setup_class['organizations_trees']['organizationId']
            get_department_res = DepartmentApi(setup_class['env']).get_department_api(data['get_department'])
            Assertions().assert_mode(get_department_res, data['get_department'])

            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 提交登记
            data['commit_register']['body']['applyEmployeeId'] = setup_class['employee_id']
            approverList = get_approval_by_organization_res.json()['data']['employeeVoList'][1]
            approverList['employeeId'] = approverList['id']
            data['commit_register']['body']['approverList'].append(approverList)
            data['commit_register']['body']['coOrgId'] = setup_class['company_id']
            data['commit_register']['body']['employeeId'] = dispatch_employee_id
            data['commit_register']['body']['workflowDeploymentId'] = workflowDeploymentId
            data['commit_register']['body']['workforceApplicationId'] = workforceApplicationId
            data['commit_register']['body']['workforceAssignRelationId'] = workforceAssignRelationId
            workforceRegistrationEmployeeBasisDto = dict()
            employee_basis = get_register_detail_res.json()['data']['workforceEmployeeManageVo']
            workforceRegistrationEmployeeBasisDto['address'] = employee_basis['address']
            workforceRegistrationEmployeeBasisDto['birthday'] = employee_basis['birthDateLong']
            workforceRegistrationEmployeeBasisDto['displayName'] = employee_basis['displayName']
            workforceRegistrationEmployeeBasisDto['emergencyMobile'] = employee_basis['employeeContactVos'][0]['mobile']
            workforceRegistrationEmployeeBasisDto['emergencyMobileAreaCode'] = employee_basis['employeeContactVos'][0]['mobileAreaCode']
            workforceRegistrationEmployeeBasisDto['emergencyName'] = employee_basis['employeeContactVos'][0]['name']
            workforceRegistrationEmployeeBasisDto['emergencyRelationshipValue'] = employee_basis['employeeContactVos'][0]['relationshipValue']
            workforceRegistrationEmployeeBasisDto['employeeCode'] = 'A' + employee_basis['employee_code']
            workforceRegistrationEmployeeBasisDto['idCard'] = employee_basis['identitys'][0]['number']
            workforceRegistrationEmployeeBasisDto['mobile'] = employee_basis['mobile']
            workforceRegistrationEmployeeBasisDto['mobileAreaCode'] = employee_basis['mobileArea']
            workforceRegistrationEmployeeBasisDto['sex'] = employee_basis['genderValue']
            workforceRegistrationEmployeeBasisDto['workforceEmployeeCode'] = employee_basis['employee_code']
            data['commit_register']['body']['workforceRegistrationEmployeeBasisDto'] = workforceRegistrationEmployeeBasisDto
            registrationPositionDto = dict()
            registrationPositionDto['attendanceNo'] = 'KQ' + employee_basis['employee_code']
            registrationPositionDto['joinTime'] = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            registrationPositionDto['lastWorkTime'] = int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            registrationPositionDto['leaderEmployeeId'] = get_department_res.json()['data']['header_employee_id']
            registrationPositionDto['leaderEmployeeName'] = get_department_res.json()['data']['header_employee_name']
            registrationPositionDto['organizationId'] = setup_class['organizations_trees']['organizationId']
            registrationPositionDto['organizationName'] = setup_class['organizations_trees']['organizationName']
            registrationPositionDto['positionId'] = setup_class['position']['positionId']
            registrationPositionDto['positionName'] = setup_class['position']['positionName']
            registrationPositionDto['projectId'] = setup_class['project']['id']
            registrationPositionDto['projectName'] = setup_class['project']['name']
            registrationPositionDto['workforceEmployeeType'] = "BLUECOLLAR"
            data['commit_register']['body']['registrationPositionDto'] = registrationPositionDto
            commit_register_res = WorkforceRegister(setup_class['env']).commit_register_api(data['commit_register'])
            Assertions().assert_mode(commit_register_res, data['commit_register'])

        with allure.step('第三步：查看登记列表员工状态'):
            # 获取登记列表
            time.sleep(6)
            data['get_register_list']['body']['coOrgId'] = setup_class['company_id']
            get_register_list_res = WorkforceRegister(setup_class['env']).get_register_list_api(
                data['get_register_list'])
            Assertions().assert_mode(get_register_list_res, data['get_register_list'])
            for item in get_register_list_res.json()['data']:
                if item['employeeId'] == dispatch_employee_id:
                    Assertions().assert_text(item['workflowStatus'], 'AGREED')
                MyLog().error('登记列表没有找到' + str(dispatch_employee_id) + '员工')

    @pytest.mark.workforce
    @allure.story("用工登记审批拒绝")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/refuse_register_approval.yaml'))
    def test_refuse_register_approval(self, data, setup_class):
        test_agree_receive_result = self.test_agree_receive(
            YamlHandle().read_yaml('SceneData/WorkforceScene/agree_receive.yaml')[0], setup_class)
        dispatch_employee_id = test_agree_receive_result

        with allure.step('第一步：设置用工登记审批流（自动审批）'):
            # 获取用工登记审批流列表
            data['get_register_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_register_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工登记审批流':
                    workflowSettingId = item['workflowSettingId']
                MyLog().error("当前公司没有生成默认登记审批流")

            # 修改默认审批流为需要上级领导审批
            data['update_register_approval_need_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_register_approval_need_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_register_approval_need_approval']['body']['workflowSettingId'] = workflowSettingId
            data['update_register_approval_need_approval']['body']['workflowSettingRuleGroupDtoList'][0][
                'workflowSettingApproverList'][0]['employeeId'] = setup_class['employee_id']
            update_register_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_register_approval_need_approval'])
            Assertions().assert_mode(update_register_approval_res, data['update_register_approval_need_approval'])

        with allure.step('第二步：登记派遣过来的员工'):
            # 获取登记列表
            data['get_register_list']['body']['coOrgId'] = setup_class['company_id']
            get_register_list_res = WorkforceRegister(setup_class['env']).get_register_list_api(data['get_register_list'])
            Assertions().assert_mode(get_register_list_res, data['get_register_list'])
            for item in get_register_list_res.json()['data']:
                if item['employeeId'] == dispatch_employee_id:
                    workforceApplicationId = item['workforceApplicationId']
                    workforceAssignRelationId = item['workforceAssignRelationId']
                MyLog().error('登记列表没有找到' + str(dispatch_employee_id) + '员工')

            # 获取登记详情
            data['get_register_detail']['params']['employeeId'] = dispatch_employee_id
            data['get_register_detail']['params']['workforceApplicationId'] = workforceApplicationId
            data['get_register_detail']['params']['workforceAssignRelationId'] = workforceAssignRelationId
            get_register_detail_res = WorkforceRegister(setup_class['env']).get_register_detail_api(data['get_register_detail'])
            Assertions().assert_mode(get_register_detail_res, data['get_register_detail'])

            # 获取部门信息
            data['get_department']['department_id'] = setup_class['organizations_trees']['organizationId']
            get_department_res = DepartmentApi(setup_class['env']).get_department_api(data['get_department'])
            Assertions().assert_mode(get_department_res, data['get_department'])

            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 提交登记
            data['commit_register']['body']['applyEmployeeId'] = setup_class['employee_id']
            approverList = get_approval_by_organization_res.json()['data']['employeeVoList'][1]
            approverList['employeeId'] = approverList['id']
            data['commit_register']['body']['approverList'].append(approverList)
            data['commit_register']['body']['coOrgId'] = setup_class['company_id']
            data['commit_register']['body']['employeeId'] = dispatch_employee_id
            data['commit_register']['body']['workflowDeploymentId'] = workflowDeploymentId
            data['commit_register']['body']['workforceApplicationId'] = workforceApplicationId
            data['commit_register']['body']['workforceAssignRelationId'] = workforceAssignRelationId
            workforceRegistrationEmployeeBasisDto = dict()
            employee_basis = get_register_detail_res.json()['data']['workforceEmployeeManageVo']
            workforceRegistrationEmployeeBasisDto['address'] = employee_basis['address']
            workforceRegistrationEmployeeBasisDto['birthday'] = employee_basis['birthDateLong']
            workforceRegistrationEmployeeBasisDto['displayName'] = employee_basis['displayName']
            workforceRegistrationEmployeeBasisDto['emergencyMobile'] = employee_basis['employeeContactVos'][0]['mobile']
            workforceRegistrationEmployeeBasisDto['emergencyMobileAreaCode'] = employee_basis['employeeContactVos'][0]['mobileAreaCode']
            workforceRegistrationEmployeeBasisDto['emergencyName'] = employee_basis['employeeContactVos'][0]['name']
            workforceRegistrationEmployeeBasisDto['emergencyRelationshipValue'] = employee_basis['employeeContactVos'][0]['relationshipValue']
            workforceRegistrationEmployeeBasisDto['employeeCode'] = 'A' + employee_basis['employee_code']
            workforceRegistrationEmployeeBasisDto['idCard'] = employee_basis['identitys'][0]['number']
            workforceRegistrationEmployeeBasisDto['mobile'] = employee_basis['mobile']
            workforceRegistrationEmployeeBasisDto['mobileAreaCode'] = employee_basis['mobileArea']
            workforceRegistrationEmployeeBasisDto['sex'] = employee_basis['genderValue']
            workforceRegistrationEmployeeBasisDto['workforceEmployeeCode'] = employee_basis['employee_code']
            data['commit_register']['body']['workforceRegistrationEmployeeBasisDto'] = workforceRegistrationEmployeeBasisDto
            registrationPositionDto = dict()
            registrationPositionDto['attendanceNo'] = 'KQ' + employee_basis['employee_code']
            registrationPositionDto['joinTime'] = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            registrationPositionDto['lastWorkTime'] = int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            registrationPositionDto['leaderEmployeeId'] = get_department_res.json()['data']['header_employee_id']
            registrationPositionDto['leaderEmployeeName'] = get_department_res.json()['data']['header_employee_name']
            registrationPositionDto['organizationId'] = setup_class['organizations_trees']['organizationId']
            registrationPositionDto['organizationName'] = setup_class['organizations_trees']['organizationName']
            registrationPositionDto['positionId'] = setup_class['position']['positionId']
            registrationPositionDto['positionName'] = setup_class['position']['positionName']
            registrationPositionDto['projectId'] = setup_class['project']['id']
            registrationPositionDto['projectName'] = setup_class['project']['name']
            registrationPositionDto['workforceEmployeeType'] = "BLUECOLLAR"
            data['commit_register']['body']['registrationPositionDto'] = registrationPositionDto
            commit_register_res = WorkforceRegister(setup_class['env']).commit_register_api(data['commit_register'])
            Assertions().assert_mode(commit_register_res, data['commit_register'])

        with allure.step('第三步：审批拒绝'):
            # 获取登记详情
            data['get_register_detail']['params']['employeeId'] = dispatch_employee_id
            data['get_register_detail']['params']['workforceApplicationId'] = workforceApplicationId
            data['get_register_detail']['params']['workforceAssignRelationId'] = workforceAssignRelationId
            get_register_detail_res = WorkforceRegister(setup_class['env']).get_register_detail_api(
                data['get_register_detail'])
            Assertions().assert_mode(get_register_detail_res, data['get_register_detail'])
            # 审批拒绝
            data['refuse_register_approvel']['body']['employeeId'] = get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            data['refuse_register_approvel']['body']['formId'] = get_register_detail_res.json()['data']['workforceAssignRelationId']
            data['refuse_register_approvel']['body']['formWorkflowId'] = get_register_detail_res.json()['data']['formWorkflowId']
            data['refuse_register_approvel']['body']['processInstanceId'] = get_register_detail_res.json()['data']['processInstanceId']
            workflow_node_approve_res = WorkflowDomain(setup_class['env']).workflow_node_approve_api(
                data['refuse_register_approvel'])
            Assertions().assert_mode(workflow_node_approve_res, data['refuse_register_approvel'])

        with allure.step('第四步：获取登记状态'):
            # 获取登记列表
            time.sleep(6)
            data['get_register_list']['body']['coOrgId'] = setup_class['company_id']
            get_register_list_res = WorkforceRegister(setup_class['env']).get_register_list_api(
                data['get_register_list'])
            Assertions().assert_mode(get_register_list_res, data['get_register_list'])
            for item in get_register_list_res.json()['data']:
                if item['employeeId'] == dispatch_employee_id:
                    Assertions().assert_text(item['workflowStatus'], "REFUSED")
                MyLog().error('登记列表没有找到' + str(dispatch_employee_id) + '员工')

    @pytest.mark.workforce
    @allure.story("用工登记审批同意")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/agree_register_approval.yaml'))
    def test_agree_register_approval(self, data, setup_class):
        test_agree_receive_result = self.test_agree_receive(
            YamlHandle().read_yaml('SceneData/WorkforceScene/agree_receive.yaml')[0], setup_class)
        dispatch_employee_id = test_agree_receive_result

        with allure.step('第一步：设置用工登记审批流（自动审批）'):
            # 获取用工登记审批流列表
            data['get_register_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_register_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工登记审批流':
                    workflowSettingId = item['workflowSettingId']
                MyLog().error("当前公司没有生成默认登记审批流")

            # 修改默认审批流为需要上级领导审批
            data['update_register_approval_need_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_register_approval_need_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_register_approval_need_approval']['body']['workflowSettingId'] = workflowSettingId
            data['update_register_approval_need_approval']['body']['workflowSettingRuleGroupDtoList'][0][
                'workflowSettingApproverList'][0]['employeeId'] = setup_class['employee_id']
            update_register_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_register_approval_need_approval'])
            Assertions().assert_mode(update_register_approval_res, data['update_register_approval_need_approval'])

        with allure.step('第二步：登记派遣过来的员工'):
            # 获取登记列表
            data['get_register_list']['body']['coOrgId'] = setup_class['company_id']
            get_register_list_res = WorkforceRegister(setup_class['env']).get_register_list_api(
                data['get_register_list'])
            Assertions().assert_mode(get_register_list_res, data['get_register_list'])
            for item in get_register_list_res.json()['data']:
                if item['employeeId'] == dispatch_employee_id:
                    workforceApplicationId = item['workforceApplicationId']
                    workforceAssignRelationId = item['workforceAssignRelationId']
                MyLog().error('登记列表没有找到' + str(dispatch_employee_id) + '员工')

            # 获取登记详情
            data['get_register_detail']['params']['employeeId'] = dispatch_employee_id
            data['get_register_detail']['params']['workforceApplicationId'] = workforceApplicationId
            data['get_register_detail']['params']['workforceAssignRelationId'] = workforceAssignRelationId
            get_register_detail_res = WorkforceRegister(setup_class['env']).get_register_detail_api(
                data['get_register_detail'])
            Assertions().assert_mode(get_register_detail_res, data['get_register_detail'])

            # 获取部门信息
            data['get_department']['department_id'] = setup_class['organizations_trees']['organizationId']
            get_department_res = DepartmentApi(setup_class['env']).get_department_api(data['get_department'])
            Assertions().assert_mode(get_department_res, data['get_department'])

            # 根据招募组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 提交登记
            data['commit_register']['body']['applyEmployeeId'] = setup_class['employee_id']
            approverList = get_approval_by_organization_res.json()['data']['employeeVoList'][1]
            approverList['employeeId'] = approverList['id']
            data['commit_register']['body']['approverList'].append(approverList)
            data['commit_register']['body']['coOrgId'] = setup_class['company_id']
            data['commit_register']['body']['employeeId'] = dispatch_employee_id
            data['commit_register']['body']['workflowDeploymentId'] = workflowDeploymentId
            data['commit_register']['body']['workforceApplicationId'] = workforceApplicationId
            data['commit_register']['body']['workforceAssignRelationId'] = workforceAssignRelationId
            workforceRegistrationEmployeeBasisDto = dict()
            employee_basis = get_register_detail_res.json()['data']['workforceEmployeeManageVo']
            workforceRegistrationEmployeeBasisDto['address'] = employee_basis['address']
            workforceRegistrationEmployeeBasisDto['birthday'] = employee_basis['birthDateLong']
            workforceRegistrationEmployeeBasisDto['displayName'] = employee_basis['displayName']
            workforceRegistrationEmployeeBasisDto['emergencyMobile'] = employee_basis['employeeContactVos'][0]['mobile']
            workforceRegistrationEmployeeBasisDto['emergencyMobileAreaCode'] = employee_basis['employeeContactVos'][0][
                'mobileAreaCode']
            workforceRegistrationEmployeeBasisDto['emergencyName'] = employee_basis['employeeContactVos'][0]['name']
            workforceRegistrationEmployeeBasisDto['emergencyRelationshipValue'] = \
            employee_basis['employeeContactVos'][0]['relationshipValue']
            workforceRegistrationEmployeeBasisDto['employeeCode'] = 'A' + employee_basis['employee_code']
            workforceRegistrationEmployeeBasisDto['idCard'] = employee_basis['identitys'][0]['number']
            workforceRegistrationEmployeeBasisDto['mobile'] = employee_basis['mobile']
            workforceRegistrationEmployeeBasisDto['mobileAreaCode'] = employee_basis['mobileArea']
            workforceRegistrationEmployeeBasisDto['sex'] = employee_basis['genderValue']
            workforceRegistrationEmployeeBasisDto['workforceEmployeeCode'] = employee_basis['employee_code']
            data['commit_register']['body'][
                'workforceRegistrationEmployeeBasisDto'] = workforceRegistrationEmployeeBasisDto
            registrationPositionDto = dict()
            registrationPositionDto['attendanceNo'] = 'KQ' + employee_basis['employee_code']
            registrationPositionDto['joinTime'] = int(
                time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')) * 1000)
            registrationPositionDto['lastWorkTime'] = int(
                time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), '%Y-%m-%d')) * 1000)
            registrationPositionDto['leaderEmployeeId'] = get_department_res.json()['data']['header_employee_id']
            registrationPositionDto['leaderEmployeeName'] = get_department_res.json()['data']['header_employee_name']
            registrationPositionDto['organizationId'] = setup_class['organizations_trees']['organizationId']
            registrationPositionDto['organizationName'] = setup_class['organizations_trees']['organizationName']
            registrationPositionDto['positionId'] = setup_class['position']['positionId']
            registrationPositionDto['positionName'] = setup_class['position']['positionName']
            registrationPositionDto['projectId'] = setup_class['project']['id']
            registrationPositionDto['projectName'] = setup_class['project']['name']
            registrationPositionDto['workforceEmployeeType'] = "BLUECOLLAR"
            data['commit_register']['body']['registrationPositionDto'] = registrationPositionDto
            commit_register_res = WorkforceRegister(setup_class['env']).commit_register_api(data['commit_register'])
            Assertions().assert_mode(commit_register_res, data['commit_register'])

        with allure.step('第三步：审批同意'):
            # 获取登记详情
            data['get_register_detail']['params']['employeeId'] = dispatch_employee_id
            data['get_register_detail']['params']['workforceApplicationId'] = workforceApplicationId
            data['get_register_detail']['params']['workforceAssignRelationId'] = workforceAssignRelationId
            get_register_detail_res = WorkforceRegister(setup_class['env']).get_register_detail_api(
                data['get_register_detail'])
            Assertions().assert_mode(get_register_detail_res, data['get_register_detail'])
            # 审批同意
            data['agree_register_approval']['body']['employeeId'] = \
            get_approval_by_organization_res.json()['data']['employeeVoList'][1]['id']
            data['agree_register_approval']['body']['formId'] = get_register_detail_res.json()['data'][
                'workforceAssignRelationId']
            data['agree_register_approval']['body']['formWorkflowId'] = get_register_detail_res.json()['data'][
                'formWorkflowId']
            data['agree_register_approval']['body']['processInstanceId'] = get_register_detail_res.json()['data'][
                'processInstanceId']
            workflow_node_approve_res = WorkflowDomain(setup_class['env']).workflow_node_approve_api(
                data['agree_register_approval'])
            Assertions().assert_mode(workflow_node_approve_res, data['agree_register_approval'])

        with allure.step('第四步：获取登记状态'):
            # 获取登记列表
            time.sleep(6)
            data['get_register_list']['body']['coOrgId'] = setup_class['company_id']
            get_register_list_res = WorkforceRegister(setup_class['env']).get_register_list_api(
                data['get_register_list'])
            Assertions().assert_mode(get_register_list_res, data['get_register_list'])
            for item in get_register_list_res.json()['data']:
                if item['employeeId'] == dispatch_employee_id:
                    Assertions().assert_text(item['workflowStatus'], "AGREED")
                MyLog().error('登记列表没有找到' + str(dispatch_employee_id) + '员工')

    @pytest.mark.workforce_smoke
    @allure.story("更新基本信息无需审批")
    @pytest.mark.parametrize('data', YamlHandle().read_yaml('SceneData/WorkforceScene/update_basic_information_without_approval.yaml'))
    def test_update_basic_information_without_approval(self, data, setup_class):
        with allure.step('第一步：设置用工更新审批流（无需审批）'):
            # 获取用工更新审批流列表
            data['get_update_approval_list']['params']['coOrgId'] = setup_class['company_id']
            get_approval_list_res = WorkflowSetApi(setup_class['env']).get_approval_list_api(
                data['get_update_approval_list'])
            for item in get_approval_list_res.json()['data']['workflowSettingVoList']:
                if item['name'] == '默认用工更新审批流':
                    workflowSettingId = item['workflowSettingId']
                MyLog().error("当前公司没有生成默认用工更新审批流")
            # 修改默认审批流为无需审批
            data['update_update_approval_without_approval']['body']['coOrgId'] = setup_class['company_id']
            data['update_update_approval_without_approval']['body']['orgIds'].append(
                setup_class['organizations_trees']['organizationId'])
            data['update_update_approval_without_approval']['body']['workflowSettingId'] = workflowSettingId
            update_apply_approval_res = WorkflowSetApi(setup_class['env']).update_approval(
                data['update_update_approval_without_approval'])
            Assertions().assert_mode(update_apply_approval_res, data['update_update_approval_without_approval'])

        with allure.step('第二步：更新员工基本信息'):
            # 根据组织节点获取对应审批流
            data['get_approval_by_organization']['organizationId'] = setup_class['organizations_trees'][
                'organizationId']
            data['get_approval_by_organization']['body']['employeeId'] = setup_class['employee_id']
            get_approval_by_organization_res = WorkflowDomain(setup_class['env']).get_approval_by_organization_api(
                data['get_approval_by_organization'])
            allure.attach(str(data['get_approval_by_organization']), "请求数据", allure.attachment_type.JSON)
            allure.attach(get_approval_by_organization_res.text, "get_approval_by_organization_api返回结果",
                          allure.attachment_type.JSON)
            Assertions().assert_mode(get_approval_by_organization_res, data['get_approval_by_organization'])
            workflowDeploymentId = get_approval_by_organization_res.json()['data']['workflowDeploymentId']

            # 根据组织获取员工列表
            data['get_organization_employee_list']['params']['organizationId'] = setup_class['organizations_trees']['organizationId']
            data['get_organization_employee_list']['params']['coOrgId'] = setup_class['company_id']
            get_update_workforce_organization_res = WorkforceOrganizationApi(setup_class['env']).get_update_workforce_organization_api(data['get_organization_employee_list'])
            Assertions().assert_mode(get_update_workforce_organization_res, data['get_organization_employee_list'])

            # 获取要修改员工的基本信息
            data['get_employee_basic']['params']['employeeId'] = get_update_workforce_organization_res.json()['data'][0]['employeechildren'][0]['id']
            get_update_employee_basic_res = WorkforceInformationUpdateApi(setup_class['env']).get_update_employee_basic_api(data['get_employee_basic'])
            Assertions().assert_mode(get_update_employee_basic_res, data['get_employee_basic'])

            # 更新基本信息
            data['update_employee_basic']['body']['applyEmployeeId'] = setup_class['employee_id']
            data['update_employee_basic']['body']['applyEmployeeName'] = 'admin'
            data['update_employee_basic']['body']['coOrgId'] = setup_class['company_id']
            data['update_employee_basic']['body']['workflowDeploymentId'] = workflowDeploymentId
            workforceEmployeeBasicDetailDto = get_update_employee_basic_res.json()['data']
            workforceEmployeeBasicDetailDto['selectEmployeeName'] = workforceEmployeeBasicDetailDto['displayname']
            workforceEmployeeBasicDetailDto['selectOrganizationId'] = setup_class['organizations_trees']['organizationId']
            workforceEmployeeBasicDetailDto['selectOrganizationName'] = setup_class['organizations_trees']['organizationName']
            workforceEmployeeBasicDetailDto['emergencyContact'] = '张三'
            workforceEmployeeBasicDetailDto['emergencyContactMobile'] = 18812341234
            workforceEmployeeBasicDetailDto['emergencyContactType'] = '父子'
            data['update_employee_basic']['body']['workforceEmployeeBasicDetailDto'] = workforceEmployeeBasicDetailDto
            post_update_employee_basic_res = WorkforceInformationUpdateApi(setup_class['env']).post_update_employee_basic_api(data['update_employee_basic'])
            Assertions().assert_mode(post_update_employee_basic_res, data['update_employee_basic'])


if __name__ == '__main__':
    pytest.main(["-sv", "test_workforce_scene_module.py::TestWorkforceScene::test_b", '-m', 'workforce', "--env", "test3"])