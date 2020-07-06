# coding:utf-8
# Name:email.py
# Author:qi.yu
# Time:2020/7/6 2:59 下午

"""
封装发送邮件的方法
"""
import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Common import consts
from Common import log
from Conf.config import Config

class SendMail:
    def __init__(self):
        self.config = Config()
        self.log = log.MyLog()

    def sendMail(self):
        msg = MIMEMultipart()
        stress_body = consts.STRESS_LIST
        result_body = consts.RESULT_LIST
        body2 = 'Hi，all\n本次接口自动化测试报告如下：\n   接口响应时间集：%s\n   接口运行结果集：%s' % (stress_body, result_body)
        mail_body2 = MIMEText(body2,_subtype='plain',_charset='utf-8')
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        msg['Subject'] = Header("接口自动化测试报告" + "_" + tm, 'utf-8')
        msg['From'] = self.config.get_conf("email","sender")
        receivers = self.config.get_conf("email","receiver")
        toclause = receivers.split(',')
        msg['to'] = ",".join(toclause)

        msg.attach(mail_body2)

        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.config.get_conf("email","smtpserver"),25)
            smtp.login(self.config.get_conf("email","username"), self.config.get_conf("email","password"))
            smtp.sendmail(self.config.get_conf("email","sender"), toclause, msg.as_string())
        except Exception as e:
            print(e)
            self.log.error("邮件发送失败，请检查邮件配置")
        else:
            self.log.info("邮件发送成功")
        finally:
            smtp.quit()