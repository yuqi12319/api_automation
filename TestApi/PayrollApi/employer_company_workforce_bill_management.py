# @Author: Saco Song
# @Time: 2020/7/27-9:22 下午
# @Description:
from TestApi.consts_api import Const


class EmployerCompanyWorkforceBillManagement(Const):

    # 获取劳务公司列表
    def get_service_company_list_api(self, url_path, data):
        url = url_path + "/dukang-coc/api/company/workforce/map"
        response = self.request.send_request_method('get', url, data['params'], headers=self.headers)
        return response

    # 获取员工所在部门面包屑
    def get_employee_department_crumb(self, url_path, data):
        url = url_path + "/dukang-employee/employees/" + data['url']['employee_id'] + "/crumb"
        response = self.request.send_request_method('get', url, headers=self.headers)
        return response

    # 获取OSS凭据
    def get_oss_credential(self, url_path, data):
        url = url_path + "/muscat/get_oss_credential"
        response = self.request.send_request_method('get', url, data['params'], headers=self.headers)
        return response

    # 上传文件至OSS
    def upload_file_to_oss(self, url_path, key, policy, oss_access_key_id, success_action_status, signature, file):
        form_data = {'key': key, 'policy': policy, 'OSSAccessKeyId': oss_access_key_id,
                     'success_action_status': success_action_status, 'signature': signature, 'file': file}
        response = self.request.send_request_method('post', url_path, headers=self.headers, files=form_data)
        return response

    # 下载附件
    def download_bill_attachment(self, url_path, destination):
        response = self.request.send_request_method('get', url_path)
        with open(destination, 'wb') as destination_file:
            destination_file.write(response.content)

    # 获取用工账单列表接口
    def get_bill_list_api(self, url_path, data):
        url = url_path + "/dukang-payroll/api/bill/list"
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response

    # 获取用工账单详情接口
    def get_bill_detail_api(self, url_path, data):
        url = url_path + "/dukang-payroll/api/bill"
        response = self.request.send_request_method('get', url, params=data['params'], headers=self.headers)
        return response

    # 获取form表单工作流和抄送信息接口
    def get_form_of_workflow_and_cc_api(self, url_path, data):
        url = url_path + "/dukang-workflow/api/form/workflow"
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response

    # 点击账单查看详情编辑账单接口
    def edit_bill_by_click_detail_api(self, url_path, data):
        url = url_path + "/dukang-payroll/api/bill"
        response = self.request.send_request_method('put', url, json=data['body'], headers=self.headers)
        return response

    # 生成用工账单（暂存）
    def generate_workforce_bill(self, url_path, data):
        url = url_path + "/dukang-Payroll/api/bill"
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response

    # 根据部门id和type获取审批流信息
    def get_approval_query_by_department_and_type_api(self, url_path, data):
        url = url_path + "/dukang-workflow/api/organizations/687335987499499520/workflow/approval/query"
        response = self.request.send_request_method('post', url, json=data['body'], headers=self.headers)
        return response

    # 获取待我审批账单个数
    def get_number_of_approval_waiting_for_me(self, url_path, data):
        url = url_path + "/dukang-payroll/api/employee/my_approve/num"
        response = self.request.send_request_method('get', url, data['params'], headers=self.headers)
        return response
