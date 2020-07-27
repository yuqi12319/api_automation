# @Author: Saco Song
# @Time: 2020/7/27-9:22 下午
# @Description:
from TestApi.consts_api import Const


class WorkforceBillManagement(Const):
    # 获取用工账单列表
    def get_bill_lists(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('post', url, data['params'], data['body'], self.headers)
        return response

    # 获取劳务公司
    def get_workforce_company_map(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('get', url, data['params'], data['body'], self.headers)
        return response
