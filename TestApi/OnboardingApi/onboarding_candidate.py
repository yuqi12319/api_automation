# @Author: Nigo Su
# @Time: 2020-08-04-11:37
# @Description:
import yaml

from TestApi.consts_api import Const


class OnboardingCandidate(Const):

    # 获取候选人列表
    def get_candidate_list_api(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('get', url, data['params'], headers=self.headers)
        return response

    # 新增候选人信息
    def post_add_candidate_api(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        # # 新增候选人id存入yaml，走入职场景
        # res = response.json()
        # with open(r"D:\python\riesling-apitest\TestData\Yaml\Onboarding\get_candidate_detail.yaml") as f:
        #     content = yaml.load(f.read(), Loader=yaml.FullLoader)
        #     content['params']['candidateId'] = '{data}'.format(**res)
        # with open(r"D:\python\riesling-apitest\TestData\Yaml\Onboarding\get_candidate_detail.yaml", 'w') as ff:
        #     yaml.dump(content, ff)
        #     ff.close()
        return response

    # 获取人员信息(包含offer和入职资料发送信息)
    def get_candidate_detail_api(self, data):
        url = self.url_path + data['url'] + '/' + str(data['params']['candidateId'])
        response = self.request.send_request_method('get', url, headers=self.headers)
        return response

    # 修改人员信息
    def put_candidate_detail_api(self, data):
        url = self.url_path + data['url'] + '/' + str(data['params']['candidateId'])
        response = self.request.send_request_method('put', url, json=data['body'], headers=self.headers)
        return response
