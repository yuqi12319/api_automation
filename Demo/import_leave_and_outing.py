# @Name:import_leave_and_outing.py
# @Author:Noah
# @Time:2020/9/8 1:35 下午

from Common.operation_mysql import *
import snowflake

class ImportLeaveAndOuting:
    def snowflake(self):
        snow = snowflake.Generator()
        id = snow.generate()
        print(id)




