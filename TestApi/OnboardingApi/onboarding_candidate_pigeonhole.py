# @Author: Nigo Su
# @Time: 2020-08-04-16:43
# @Description:
from TestApi.consts_api import Const


class OnboardingCandidatePigeonhole(Const):

    # 操作人员归档
    def put_candidate_pigeonhole_api(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('put', url, data['params'], headers=self.headers)
        return response

    # 获取归档人员列表
    def get_pigeonhole_list_api(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('get', url, data['params'], headers=self.headers)
        return response

    # 还原归档人员
    def put_pigeonhole_reduction_api(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('put', url, data['params'], headers=self.headers)
        return response
