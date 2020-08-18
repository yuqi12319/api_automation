# Name:workforce_workflow.py.py
# Author:lin
# Time:2020/8/5 10:28 上午


from TestApi.consts_api import Const


class WorkforceWorkflow(Const):
    def __init__(self, env):
        super().__init__(env)

    def workflow_application_await_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    def workflow_application_cc_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    def workflow_application_pass_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    def workflow_application_refuse_list_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res

    # 节点审批(同意，拒绝)
    def workflow_node_approve_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 批量节点审批(同意，拒绝)
    def workflow_batch_node_approve_api(self, data):
        url = self.url_path + data['url']
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res

    # 已有公司添加默认用工申请审批流
    def application_workflow_setting_default_api(self, data):
        url = self.url_path + data['url']
        print(url)
        res = self.request.send_request_method('post', url=url, params=data['params'], headers=self.headers)
        return res