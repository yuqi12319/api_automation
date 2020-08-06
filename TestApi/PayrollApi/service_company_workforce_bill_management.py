# @Author: Saco Song
# @Time: 2020/8/5-2:51 下午
# @Description:
from TestApi.consts_api import Const


class ServiceCompanyWorkforceBillManagement(Const):

    # 提出账单异议
    def submit_dissent_workforce_bill_form(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('put', url, json=data['body'], headers=self.headers)
        return response

    # 获取劳务工账单列表接口
    def get_workforce_bill_list_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('post', url, params=data['params'], headers=self.headers)
        return response
