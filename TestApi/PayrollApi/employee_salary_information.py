# @Name:employee_salary_information.py
# @Author:Noah
# @Time:2020/8/6 1:59 下午
from TestApi.consts_api import Const

class EmployeeSalaryInformation(Const):

    # 获取员工薪资信息列表表头接口
    def get_employee_salary_information_list_head_api(self, url_path, data):
        url = url_path + "/dukang-payroll/employee/salary/head"
        response = self.request.send_request_method('get', url, params=data['params'], headers=self.headers)
        return response

    # 获取员工薪资信息列表接口
    def get_employee_salary_information_list_api(self, url_path, data):
        url = url_path + "/dukang-payroll/employee/salaryList"
        self.headers["X-Page-Size"] = "20"
        self.headers["x-current-page"] = "1"
        response = self.request.send_request_method('post', url, params=data['params'], json=data['body'], headers=self.headers)
        return response

    # 获取薪资信息个税主体和分部门列表
    def get_itEntitys_and_departments_list_api(self, url_path, data):
        url = url_path + "/dukang-its/payroll/itEntitys"
        response = self.request.send_request_method('get', url, params=data['params'], headers=self.headers)
        return response






