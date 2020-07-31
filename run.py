# coding:utf-8
# Name:run.py
# Author:qi.yu
# Time:2020/6/26 9:19 上午

import pytest
from Common.shell import Shell
from Conf.config import Config
from Common.log import MyLog

if __name__ == '__main__':
    conf = Config()
    log = MyLog()
    shell = Shell()
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path

    # 定义测试集
    args = ['-s', '-q', '--alluredir', xml_report_path, './TestCase/TestWorkforce/']
    pytest.main(args)

    cmd = 'allure generate %s -o %s' % (xml_report_path, html_report_path)

    try:
        shell.invoke(cmd)
    except Exception:
        log.error('执行测试用例失败')
        raise
    #
    # try:
    #     mail = Email.SendMail()
    #     mail.sendMail()
    # except Exception as e:
    #     log.error('发送邮件失败，请检查邮件配置')
    #     raise