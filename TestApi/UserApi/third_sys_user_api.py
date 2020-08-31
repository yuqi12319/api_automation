# Name:third_sys_user_api.py
# Author:lin
# Time:2020/8/25 5:48 下午

from TestApi.consts_api import Const


class ThirdSysUserApi(Const):

    def __init__(self, env):
        super().__init__(env)

    def test_active_employee_register(self, data):
        url = 'https://dktest3-freesia.bipocloud.com/services/dukang-user/users/activeEmployeeRegister'
        res = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return res

    # 修改手机号
    def change_phone_number_api(self, data):
        url = self.url_path + '/dukang-user/phoneNumber/change'
        res = self.request.send_request_method('put', url=url, json=data['body'], headers=self.headers)
        return res
