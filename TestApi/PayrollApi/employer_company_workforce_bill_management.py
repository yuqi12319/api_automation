# @Author: Saco Song
# @Time: 2020/7/27-9:22 下午
# @Description:
from TestApi.consts_api import Const


class WorkforceBillManagement(Const):

    # 获取劳务公司列表
    def get_service_company_list_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('get', url, data['params'], headers=self.headers)
        return response

    # 获取员工所在部门面包屑
    def get_employee_department_crumb(self, url_path, data):
        url = url_path + data['url']['first_half'] + data['url']['employee_id'] + data['url']['second_half']
        response = self.request.send_request_method('get', url, headers=self.headers)
        return response

    # 获取OSS凭据
    def get_oss_credential(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('get', url, data['params'], headers=self.headers)
        return response

    # 上传文件至OSS
    def upload_file_to_oss(self, url_path, files):
        response = self.request.send_request_method('post', url_path, headers=self.headers, files=files)
        return response

    # 获取用工账单列表接口
    def get_bill_list_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('post', url, json = data['body'], headers = self.headers)
        return response

    # 获取用工账单详情接口
    def get_bill_detail_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('get', url, params = data['params'], headers = self.headers)
        return response

    # 获取form表单工作流和抄送信息接口
    def get_form_of_workflow_and_cc_api(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('post', url, json = data['body'], headers = self.headers)
        return response

    # 生成用工账单（暂存）
    def generate_workforce_bill(self, url_path, data):
        url = url_path + data['url']
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response
#
# # 根据部门id和type获取审批流信息
# def get_approval_query_api(self, url_path, data):
#     url = url_path + data['url_first_half'] + data['organization_id'] + data['url_second_half']
#     response = self.request.send_request_method('get', url, data['params'], data['body'], self.headers)
#     return response
