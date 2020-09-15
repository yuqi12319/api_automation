# coding:utf-8
# Name:employee_api.py
# Author:qi.yu
# Time:2020/8/26 5:46 下午
# Description:

from TestApi.consts_api import Const


class EmployeeApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def brief_profile_api(self, data):
        url = self.url_path + '/dukang-employee/employees/brief_profile'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取员工管理列表数据接口
    def get_employee_manager_list(self, data):
        url = self.url_path + '/dukang-employee/employees/manage'
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=data['headers'])
        return res

    # 获取员工信息（组织信息）接口
    def get_employee_organization_api(self, data):
        url = self.url_path + '/dukang-employee/employees/' + data['employee_id'] + '/organization'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取员工信息（个人信息）接口
    def get_employee_information_api(self, data):
        url = self.url_path + '/dukang-employee/employees/' + data['employee_id'] + '/profile'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res

    # 获取员工信息（教育信息）接口
    def get_employee_education_api(self, data):
        url = self.url_path + '/dukang-employee/employees/' + data['employee_id'] + '/education'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res

    # 获取员工信息（工作经历）接口
    def get_employee_work_experience_api(self, data):
        url = self.url_path + '/dukang-employee/employees/' + data['employee_id'] + '/work'
        res = self.request.send_request_method('get', url=url, headers=self.headers)
        return res

    # 修改员工信息（组织信息）接口
    def update_employee_organization_api(self, data):
        url = self.url_path + '/dukang-employee/employees/' + data['employee_id'] + '/organization'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 修改员工信息（个人信息）接口
    def update_employee_information_api(self, data):
        url = self.url_path + '/dukang-employee/employees/profile'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 修改员工信息（教育信息）接口
    def update_employee_education_api(self, data):
        url = self.url_path + '/dukang-employee/employees/education'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 修改员工信息（工作经历）接口
    def update_employee_work_experience_api(self, data):
        url = self.url_path + '/dukang-employee/employees/work'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 查询用户当前公司所有审批任务列表（我的审批）
    def my_approval_api(self, data):
        url = self.url_path + '/dukang-employee/employee/approval_list'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 我的申请
    def my_application_api(self, data):
        url = self.url_path + '/dukang-employee/employee/application_list'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
