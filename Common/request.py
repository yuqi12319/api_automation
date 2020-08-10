# coding:utf-8
# Name:request.py
# Author:qi.yu
# Time:2020/6/25 6:35 下午

import requests
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

    def get_requests(self, url, params=None, headers=None, cookies=None, timeout=TIMEOUT):
        """
        get请求
        :param url:
        :param params:
        :param headers:
        :param cookies:
        :param timeout:
        :return:
        """
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = '%s%s' % ('http://', url)

        try:
            response = requests.get(url=url, params=params, headers=headers, cookies=cookies, timeout=timeout,
                                    verify=False)
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")

        time_consuming = response.elapsed.microseconds / 1000  # time_consuming为响应时间，单位为毫秒
        Common.consts.STRESS_LIST.append(time_consuming)
        if self.is_json(response.text):
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (
                url, response.request.body, response.json(), response.status_code))
        else:
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (
                url, response.request.body, response.status_code))
        return response

    def post_requests(self, url, params=None, json=None, headers=None, cookies=None, timeout=TIMEOUT, files=None):
        """
        post请求
        :param url:
        :param params:
        :param json:
        :param headers:
        :param cookies:
        :param timeout:
        :param files:
        :return:
        """
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = '%s%s' % ('http://', url)

        try:
            response = requests.post(url=url, params=params, json=json, headers=headers, cookies=cookies,
                                     timeout=timeout,
                                     verify=False, files=files)
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")

        time_consuming = response.elapsed.microseconds / 1000
        Common.consts.STRESS_LIST.append(time_consuming)
        if self.is_json(response.text):
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (
                url, response.request.body, response.json(), response.status_code))
        else:
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (
                url, response.request.body, response.status_code))
        return response

    def put_requests(self, url, params=None, json=None, headers=None, cookies=None, timeout=TIMEOUT):
        """
        put请求
        :param url:
        :param params:
        :param json:
        :param headers:
        :param cookies:
        :param timeout:
        :return:
        """
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = '%s%s' % ('http://', url)

        try:
            response = requests.put(url=url, params=params, json=json, headers=headers, cookies=cookies,
                                    timeout=timeout, verify=False)
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")

        time_consuming = response.elapsed.microseconds / 1000
        Common.consts.STRESS_LIST.append(time_consuming)
        if self.is_json(response.text):
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (
                url, response.request.body, response.json(), response.status_code))
        else:
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (
                url, response.request.body, response.status_code))
        return response

    def delete_requests(self, url, params=None, json=None, headers=None, cookies=None, timeout=TIMEOUT):
        """
        delete请求
        :param url:
        :param params:
        :param json:
        :param headers:
        :param cookies:
        :param timeout:
        :return:
        """
        if url.startswith('http://') or url.startswith('https://'):
            pass
        else:
            url = '%s%s' % ('http://', url)

        try:
            response = requests.delete(url=url, params=params, json=json, headers=headers, cookies=cookies,
                                    timeout=timeout, verify=False)
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")

        time_consuming = response.elapsed.microseconds / 1000
        Common.consts.STRESS_LIST.append(time_consuming)
        if self.is_json(response.text):
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (
                url, response.request.body, response.json(), response.status_code))
        else:
            self.log.info("URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (
                url, response.request.body, response.status_code))
        return response

    def send_request_method(self, method, url, params=None, json=None, headers=None, files=None):
        if headers is None:
            headers = {'Content-type': "application/json",
                       "Authorization": ""}

        if method in ['get', 'GET']:
            response = self.get_requests(url=url, params=params, headers=headers)
        elif method in ['post', 'POST']:
            response = self.post_requests(url=url, params=params, json=json, headers=headers, files=files)
        elif method in ['put', 'PUT']:
            response = self.put_requests(url, params=params, json=json, headers=headers)
        elif method in ['delete', 'DELETE']:
            response = self.delete_requests(url=url, params=params, json=json, headers=headers)
        else:
            self.log.error("request method error")

        return response