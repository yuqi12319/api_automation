# @Author: Saco Song
# @Time: 2020/9/8-11:33 上午
# @Description:
import time
from datetime import datetime

import pymysql

from Common.operation_mysql import mysqlDict
from Common.snowflake import Generator
from Demo.mysql_util import get_employee_ids


class ImportDailyAndOvertimeRelatedData:

    @staticmethod
    def time_shifter(from_time, displacement, unit='s'):
        if unit == 's':

            return datetime.strptime()

            # return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
            #     time.mktime(time.strptime(from_time, '%Y-%m-%d %H:%M:%S')) + displacement))
        elif unit == 'm':
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                time.mktime(time.strptime(from_time, '%Y-%m-%d %H:%M:%S')) + displacement * 60))
        elif unit == 'h':
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                time.mktime(time.strptime(from_time, '%Y-%m-%d %H:%M:%S')) + displacement * 3600))
        else:
            return from_time

    def import_overtime_form(self, database, attendance_group_id, start_date, end_date):
        query_data = []
        employee_ids = get_employee_ids(database, attendance_group_id)
        id_generator = Generator()
        current_date = start_date

        for employee in employee_ids:
            while current_date <= end_date:
                primary_key_id = id_generator.generate()
                start_time = self.time_shifter(current_date, 19, 'h')
                end_time = self.time_shifter(start_time, 2, 'h')
                duration = time.strptime(end_time, '%Y-%m-%d %H:%M:%S') - time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                query_data.append()

        # insert_sql = "INSERT INTO overtime_form (id,attendance_group_id,attendance_group_type,shift_id,employee_id," \
        #              "overtime_date,start_time,end_time,duration,`status`,deleted,created_time) VALUES (%d," \
        #              "748596799903629312,'FIXED',748596799903629316,%d,%s,%s,%s,%d,'AGREED',0,%s)"
        #
        # db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
        #                      database=database, charset='utf8')
        # cursor = db.cursor()
        # try:
        #     cursor.executemany(insert_sql, insert_args)
        #     db.commit()
        # except Exception as e:
        #     db.rollback()
        #     return e
        #
        # cursor.close()
        # db.close()
        # return data


if __name__ == '__main__':
    im = ImportDailyAndOvertimeRelatedData()
    # im.import_overtime_form('dukang_attendance_dktest2', 748596799903629312)
