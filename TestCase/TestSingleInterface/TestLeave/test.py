# Name:test.py
# Author:michelle.hou
# Time:2020-08-14 14:14
import datetime
import time

from Common.operation_yaml import YamlHandle

day_time = int(time.mktime(datetime.date.today().timetuple()))
print(int(round(day_time * 1000)))
stamp = int(round(day_time * 1000))
a = YamlHandle().read_yaml('Leave/LeaveForm/leave_form_by_day_apply.yaml')
print(a)
print(type(a))
b = a[0]['body']['beginDate']
print(b)

# YamlHandle().write_yaml('Leave/LeaveForm/leave_form_by_day_apply.yaml',, stamp)
