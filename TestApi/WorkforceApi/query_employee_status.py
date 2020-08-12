# Name:query_employee_status.py
# Author:lin
# Time:2020/7/29 3:21 下午

from TestApi.consts_api import Const


class QueryEmployeeStatus(Const):
    def __init__(self, env):
        super().__init__(env)

    def test_query_status(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method(method='get', url=url, params=data['body'], headers=self.headers)
        return res
