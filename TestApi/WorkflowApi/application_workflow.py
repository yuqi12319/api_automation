# Name:application_workflow.py.py
# Author:lin
# Time:2020/8/5 10:28 上午


from TestApi.consts_api import Const


class ApplicationWorkflow(Const):
    def __init__(self):
        super().__init__()

    def workfolw_application(self, url_path, data, style):
        if style == 'await':
            url = url_path + data['url']
        elif style == 'cc':
            url = url_path + data['url_cc']
        elif style == 'pass':
            url = url_path + data['url_pass']
        else:
            url = url_path + data['url_refuse']
        res = self.request.send_request_method('post', url=url, params=data['params'], json=data['body'],
                                               headers=self.headers)
        return res
