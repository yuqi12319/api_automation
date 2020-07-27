# @Author: Saco Song
# @Time: 2020/7/27-9:22 下午
# @Description:
from TestApi.consts_api import Const


class WorkforceBillManagement(Const):
    # 获取用工账单列表
    def get_bill_lists(self, url_path, data):
        url = url_path + data['url']
        res = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return res


