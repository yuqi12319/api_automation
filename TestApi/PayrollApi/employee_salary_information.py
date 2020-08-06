# @Name:employee_salary_information.py
# @Author:Noah
# @Time:2020/8/6 1:59 下午
from TestApi.consts_api import Const

class EmployeeSalaryInformation(Const):

    # 获取员工薪资信息列表表头接口
    def get_employee_salary_information_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('get', url, params=data['params'], headers=self.headers)
        return response




