# Name:init_payrollItem.py
# Author:lin
# Time:2020/8/3 3:42 下午


from TestApi.consts_api import Const


class InitPayrollItem(Const):

    def __init__(self):
        super().__init__()

    ## 新建公司时，初始化薪资项
    def init_payrollItem(self, url_path, data):
        url = url_path + data['url'] + str(data['body']['coOrgId'])
        print(url)
        res = self.request.send_request_method('post', url=url, params=data['body'], headers=self.headers)
        return res
