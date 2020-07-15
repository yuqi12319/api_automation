# coding:utf-8
# Name:request.py
# Author:qi.yu
# Time:2020/6/25 6:35 下午

import requests
from requests.models import Response

import Common.consts
from Common import log
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

TIMEOUT = 60


class Request:

    def __init__(self):
        self.log = log.MyLog()

    def is_json(self, obj):
        try:
            json.loads(obj)
        except ValueError as e:
            return False
        return True

    def get_requests(self, url, data=None, headers=None, cookies=None, timeout=TIMEOUT):
        """
        get请求
        :param url:
        :param data:
        :param header:
        :return:
        """
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = '%s%s' % ('http://', url)

        try:
            response = requests.get(url=url, params=data, headers=headers, cookies=cookies, timeout=timeout,
                                    verify=False)
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")

        time_consuming = response.elapsed.microseconds / 1000  # time_consuming为响应时间，单位为毫秒
        time_total = response.elapsed.total_seconds()  # time_total为响应时间，单位为秒
        Common.consts.STRESS_LIST.append(time_consuming)
        response_dicts = dict()
        response_dicts['code'] = response.status_code
        if self.is_json(response.text):
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (
                url, response.request.body, response.json(), response.status_code))
        else:
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (
                url, response.request.body, response.status_code))
        response_dicts['json'] = response.json()
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        return response_dicts

    def post_requests(self, url, data=None, headers=None, cookies=None, timeout=TIMEOUT):
        """
        post请求
        :param url:
        :param data:
        :param header:
        :return:
        """
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = '%s%s' % ('http://', url)

        try:
            response = requests.post(url=url, json=data, headers=headers, cookies=cookies, timeout=timeout, verify=False)
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()
        Common.consts.STRESS_LIST.append(time_consuming)
        response_dicts = dict()
        if response.status_code == 200:
            response_dicts['code'] = response.status_code
            if self.is_json(response.text):
                self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (
                    url, response.request.body, response.json(), response.status_code))
            else:
                self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (
                    url, response.request.body, response.status_code))
            response_dicts['json'] = response.json()
            response_dicts['time_consuming'] = time_consuming
            response_dicts['time_total'] = time_total
            return response_dicts
        else:
            print(response.status_code)
            self.log.error('request status_code error: ')
            raise

    def put_requests(self, url, data=None, headers=None, cookies=None, timeout=TIMEOUT):
        """
        put请求
        :param url:
        :param data:
        :param header:
        :return:
        """
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = '%s%s' % ('http://', url)

        try:
            response = requests.put(url=url, json=data, headers=headers, cookies=cookies, timeout=timeout, verify=False)
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()
        Common.consts.STRESS_LIST.append(time_consuming)
        response_dicts = dict()
        response_dicts['code'] = response.status_code
        if self.is_json(response.text):
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (
                url, response.request.body, response.json(), response.status_code))
        else:
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (
                url, response.request.body, response.status_code))
        response_dicts['json'] = response.json()
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        return response_dicts

    def send_request_method(self, method, url, data=None, headers=None, timeout=TIMEOUT):
        if headers is None:
            headers = {
                'Content-type': 'application/json',
                'Authorization': ''
            }
            headers = {'Content-type': "application/json",
                       "Authorization": ""}

        if method in ['get', 'GET']:
            response = Request().get_requests(url,data,headers)
        elif method in ['post', 'POST']:
            response = Request().post_requests(url,data,headers)
        elif method in ['put', 'PUT']:
            response = Request.put_requests(url,data,headers)
        else:
            self.log.error("request method error")

        return response


if __name__ == '__main__':
    a = Request()
    b = a.get_requests("https://baidu.com")
    print(b['time_consuming'])
