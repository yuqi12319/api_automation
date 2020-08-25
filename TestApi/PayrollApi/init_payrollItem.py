# Name:init_payrollItem.py
# Author:lin
# Time:2020/8/3 3:42 下午


from TestApi.consts_api import Const


class InitPayrollItem(Const):

    def __init__(self, env):
        super().__init__(env)

    # 新建公司时，初始化薪资项
    def init_payrollItem(self, data):
        url = self.url_path + '/dukang-payroll/init/payrollItem/' + str(data['body']['coOrgId'])
        res = self.request.send_request_method('post', url=url, params=data['body'], headers=self.headers)
        return res
