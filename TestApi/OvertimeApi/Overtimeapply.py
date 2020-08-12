from TestApi.consts_api import Const


class OvertimeApply(Const):

    # def __init__(self):
    #     self.request = Request()
    #     self.access_token = YamlHandle().read_yaml('login.yaml')[0]['accessToken']

    # 加班申请接口
    def send_apply_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response

    def send_get_overtime_detail(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('get', url, params=data['params'], headers=self.headers)
        return response
