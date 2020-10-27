# coding:utf-8
# Name:organization.py
# Author:qi.yu
# Time:2020/10/26 4:28 下午
# Description:

import time
from TestApi.MuscatApi.department_api import DepartmentApi
from TestApi.MuscatApi.organization_business_level_api import OrganizationBusinessLevelApi


# 新增部门
def add_department(env, businessType, company_id, level_name, parent_id):
    global organizationBusinessLevelId
    global name
    workforce_level = {
        '总部': 0,
        '大区': 1,
        '仓库': 2,
        '项目组': 3,
        '小组': 4
    }
    commission_level = {
        '总部': 0,
        '大区': 1,
        '门店': 2
    }
    get_organization_business_level_data = dict()
    get_organization_business_level_data['params'] = dict()
    get_organization_business_level_data['params']['coOrgId'] = company_id
    get_organization_business_level_data['params']['type'] = businessType
    get_organization_business_level_res = OrganizationBusinessLevelApi(env).get_organization_business_level_api(
        get_organization_business_level_data)
    if businessType == 'GENERALDEPARTMENT':
        name = '普通部门' + str(int(time.time()))
    if businessType == 'WORKFORCE':
        name = '用工部门' + str(int(time.time()))
        organizationBusinessLevelId = get_organization_business_level_res.json()['data'][workforce_level[level_name]][
            'id']
    if businessType == 'COMMISSION':
        name = '绩效部门' + str(int(time.time()))
        organizationBusinessLevelId = get_organization_business_level_res.json()['data'][commission_level[level_name]][
            'id']
    add_department_data = dict()
    add_department_data['body'] = dict()
    add_department_data['body']['businessType'] = businessType
    add_department_data['body']['code'] = ''
    add_department_data['body']['name'] = name
    add_department_data['body']['organizationBusinessLevelId'] = organizationBusinessLevelId
    add_department_data['body']['parent_id'] = parent_id
    add_department_res = DepartmentApi(env).add_department_api(add_department_data)
    return add_department_res
