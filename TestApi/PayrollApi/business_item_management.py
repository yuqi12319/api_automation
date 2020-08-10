# @Author: Saco Song
# @Time: 2020/8/6-1:36 下午
# @Description:
from TestApi.consts_api import Const


class BusinessItemManagement(Const):

    # 新增保存业务项目
    def save_business_item(self, url_path, data):
        url = url_path + "/dukang-payroll/business_item"
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response
