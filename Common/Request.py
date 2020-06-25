# coding:utf-8
# Name:Request.py
# Author:qi.yu
# Time:2020/6/25 6:35 下午

import requests
import json
import urllib3

TIMEOUT = 60

class Request:
    def __init__(self):
        pass

    def is_json(self,obj):
        try:
            json.loads(obj)
        except ValueError as e:
            return False
        return True

    def send_request_method(self,method,url,data=None,headers=None,timeout=TIMEOUT):
        if not url.startswith('http://'):
            url = "s%s" % ('http://',url)
        if headers is None:
            headers = {'Content-type': "application/json",
                       "Authorization": ""}
        try:
            if method in ['get','GET']:
                response = requests.get(url=url,json=data,headers=headers,timeout=timeout,verify=False)
            elif method in ['post','POST']:
                response = requests.post(url=url,json=data,headers=headers,timeout=timeout,verify=False)
            elif method in ['put','PUT']:
                response = requests.put(url=url,json=data,headers=headers,timeout=timeout,verify=False)

            if self.is_json(response.text):
                print("[%s] URL: %s \n[REQUEST BODY]:%s \n[RESPONSE]:%s \n[CODE]: %s" % (method, url, response.request.body, response.json(), response.status_code))
            else:
                print("[%s] URL: %s \n[REQUEST BODY]:%s \n[RESPONSE EMPTY] \n[CODE]: %s" % (method, url, response.request.body, response.status_code))
            return response
        except requests.exceptions.ConnectTimeout:
            raise Exception("CONNECTION_TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise Exception("CONNECTION_ERROR")
        except urllib3.exceptions.ProtocolError:
            raise Exception("CONNECTION_ERROR")