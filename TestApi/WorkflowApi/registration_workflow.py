# Name:application_workflow.py.py
# Author:lin
# Time:2020/8/13 10:28 上午


from TestApi.consts_api import Const


class Workflow(Const):
    def __init__(self, env):
        super().__init__(env)

    def workflow_registration_await_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    def workflow_registration_cc_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    def workflow_registration_pass_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    def workflow_registration_refuse_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res