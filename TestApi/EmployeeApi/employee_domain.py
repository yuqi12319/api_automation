# Name:employee_domain.py.py
# Author:lin
# Time:2020/8/27 10:52 上午


from TestApi.consts_api import Const


class EmployeeDomain(Const):

    def __init__(self, env):
        super().__init__(env)

    # 获取未激活员工集合
    def employee_unactice(self, data):
        url = self.url_path + '/dukang-employee/employee/unActive'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=data['headers'])
        return res

    # 判断该手机号是否能通过链接加入公司
    def check_active_mobile(self, data):
        url = 'https://dktest3-freesia.bipocloud.com/services/dukang-employee/invitation/checkActiveMobile'
        res = self.request.send_request_method('post', url=url, params=data['params'], headers=self.headers)
        return res

    # 激活员工
    def invitation_active_employee(self, data):
        url = self.url_path + '/dukang-employee/invitation/activeEmployee'
        res = self.request.send_request_method('post', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取激活链接
    def active_QRcode(self, data):
        url = self.url_path + '/dukang-employee/invitation/activeQRcode'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 批量导入员工信息(导入excel)
    def batch_import_employee(self, data, files):
        url = self.url_path + '/dukang-employee/batch/importEmployees'
        res = self.request.send_request_method('post', url=url, params=data['params'], files=files,
                                               headers=self.headers)
        return res

    # 获取excel中导入的员工信息
    def batch_import_employee_1(self, data):
        url = self.url_path + '/dukang-employee/batch/importEmployees'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=data['headers'])
        return res

    # 确认导入员工信息
    def correct_employee(self, data):
        url = self.url_path + '/dukang-employee/batch/correctEmployees'
        res = self.request.send_request_method('post', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取部门下所有子部门信息
    def organizations_children(self, data):
        url = self.url_path + '/muscat/organizations/' + str(data['coOrgId']) + '/children'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 获取公司组织架构
    def organizations_chart(self, data):
        url = self.url_path + '/muscat/organizations/' + str(data['coOrgId']) + '/chart'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 修改公司信息（设置公司主管）
    def modify_companies(self, data):
        url = self.url_path + '/muscat/companies' + '/' + str(data['coOrgId'])
        res = self.request.send_request_method('put', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    # 获取层级结构
    def departments_level(self, data):
        url = self.url_path + '/muscat/organization_business_level'
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res

    # 新增部门
    def departments(self, data):
        url = self.url_path + '/muscat/departments'
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res
