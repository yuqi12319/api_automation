# coding:utf-8


"""
封装Assert方法
"""

from Common import log
import Common.consts
import json

class Assertions:
    def __init__(self):
        self.log = log.MyLog()

    def assert_code(self,code,expected_code):
        """
        验证response状态码
        :param code
        :param expected_code
        :return:
        """
        try:
            assert code == expected_code
            Common.consts.RESULT_LIST.append('True')
            return True
        except:
            self.log.error("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))
            Common.consts.RESULT_LIST.append('fail')

            raise

    def assert_body(self,body,body_msg,expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param excepted_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            Common.consts.RESULT_LIST.append('True')
            return True
        except:
            self.log.error("Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, body_msg))
            Common.consts.RESULT_LIST.append('fail')

            raise

    def assert_in_text(self,body,expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body,ensure_ascii=False)
            assert expected_msg in text
            Common.consts.RESULT_LIST.append('True')
            return True
        except:
            self.log.error("Response body Does not contain expected_msg, expected_msg is %s" % expected_msg)
            Common.consts.RESULT_LIST.append('fail')

            raise

    def assert_text(self,body,expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg
            Common.consts.RESULT_LIST.append('True')
            return True
        except:
            self.log.error("Response body != expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))
            Common.consts.RESULT_LIST.append('fail')

    def assert_time(self,time,expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param time:
        :param expected_time:
        :return:
        """
        try:
            assert time < expected_time
            Common.consts.RESULT_LIST.append('True')
            return True
        except:
            self.log.error("Response time > expected_time, expected_time is %s, time is %s" % (expected_time, time))
            Common.consts.RESULT_LIST.append('fail')

            raise