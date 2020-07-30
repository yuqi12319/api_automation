from Common.request import Request
from Common.operation_yaml import YamlHandle
import time


class OvertimeApply:

    def __init__(self):
        self.request = Request()
        self.access_token = YamlHandle().read_yaml('login.yaml')[0]['accessToken']
        self.get_data = time.time()
        self.t = int(round(self.get_data * 1000))

# 加班申请接口
    def send_apply_api(self, url_path, data):
        url = url_path + data['url']
        headers = data['headers']
        headers.update({'X-Dk-Token': self.access_token})
        res = self.request.send_request_method('post', url, data['body'], headers)
        return res

    def send_get_overtime_detail(self, url_path, data):
        url = url_path + data['url'] + self.t
        headers = data['headers']
        headers.update({'X-Dk-Token': self.access_token})
        res = self.request.send_request_method('get', url, data['body'], headers)
        return res
