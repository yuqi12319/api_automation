# @Name:employee_salary_information.py
# @Author:Noah
# @Time:2020/8/6 1:59 下午
from TestApi.consts_api import Const

class EmployeeSalaryInformation(Const):

    # 获取员工薪资信息列表表头接口
    def get_employee_salary_information_list_head_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('get', url, params=data['params'], headers=self.headers)
        return response

    # 获取员工薪资信息列表接口
    def get_employee_salary_information_list_api(self, url_path, data):
        url = url_path + data['url']
        extra_headers = {"X-Page-Size": "20", "x-current-page": "1"}
        self.headers["X-Page-Size"] = "20"
        self.headers["x-current-page"] = "1"
        response = self.request.send_request_method('post', url, params=data['params'], json=data['body'], headers=self.headers)
        print(response.headers)
        return response





