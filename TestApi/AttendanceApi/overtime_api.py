from TestApi.consts_api import Const


class OvertimeApi(Const):

    def __init__(self, env):
        super().__init__(env)

    # 加班申请接口
    def send_overtime_apply_api(self, data):
        url = self.url_path + '/dukang-attendance/api/overtime'
        response = self.request.send_request_method('post', url=url, json=data['body'], headers=self.headers)
        return response

    def send_get_overtime_detail(self, data):
        url = self.url_path + data['url']
        response = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return response

    # 查询加班申请时间是否符合条件
    def check_overtime(self, data):
        url = self.url_path + '/dukang-attendance/api/checkovertime?attendanceGroupId=&overtimeDate=&&shiftId='
        res = self.request.send_request_method('get', url=url, params=data['params'], headers=self.headers)
        return res
