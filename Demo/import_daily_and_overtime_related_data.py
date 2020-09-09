# @Author: Saco Song
# @Time: 2020/9/8-11:33 上午
# @Description:
import time
from datetime import datetime, timedelta

import pymysql

from Common.operation_mysql import mysqlDict
from Common.snowflake import Generator
from Demo.mysql_util import get_employee_ids


class ImportDailyAndOvertimeRelatedData:
    date_format = '%Y-%m-%d %H:%M:%S'

    def time_shifter(self, from_time, displacement, unit='s'):
        if unit == 's':
            temp_datetime = (datetime.strptime(from_time, self.date_format))
            temp_datetime += timedelta(seconds=displacement)
            return temp_datetime.strftime(self.date_format)
        elif unit == 'm':
            temp_datetime = (datetime.strptime(from_time, self.date_format))
            temp_datetime += timedelta(minutes=displacement)
            return temp_datetime.strftime(self.date_format)
        elif unit == 'h':
            temp_datetime = (datetime.strptime(from_time, self.date_format))
            temp_datetime += timedelta(hours=displacement)
            return temp_datetime.strftime(self.date_format)
        elif unit == 'd':
            temp_datetime = (datetime.strptime(from_time, self.date_format))
            temp_datetime += timedelta(days=displacement)
            return temp_datetime.strftime(self.date_format)
        else:
            return from_time

    def import_overtime_form(self, database, attendance_group_id, shift_id, start_date, end_date):
        query_data = []
        employee_ids = get_employee_ids(database, attendance_group_id)
        id_generator = Generator()
        current_date = start_date

        for employee in employee_ids:
            while current_date <= end_date:
                primary_key_id = int(id_generator.generate())
                start_time = self.time_shifter(current_date, 19, 'h')
                end_time = self.time_shifter(start_time, 2, 'h')
                duration = int((datetime.strptime(end_time, self.date_format)
                                - datetime.strptime(start_time, self.date_format)).seconds)
                created_time = (datetime.strptime(current_date, self.date_format) - timedelta(days=1)).strftime(
                    self.date_format)
                updated_time = datetime.today().strftime(self.date_format)
                query_data.append(
                    (primary_key_id, attendance_group_id, shift_id, employee, current_date, start_time, end_time,
                     duration, created_time, updated_time))

                current_date = self.time_shifter(current_date, 1, 'd')

            current_date = start_date

        for data in query_data:
            print(data)

        insert_sql = "INSERT INTO overtime_form (id, attendance_group_id, attendance_group_type, shift_id, " \
                     "employee_id, overtime_date, start_time, end_time, duration, `status`, deleted, created_time, " \
                     "updated_time) VALUES (%s, %s, 'FIXED', %s, %s, %s, %s, %s, %s, 'AGREED', 0, %s, %s)"

        db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
                             database=database, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.executemany(insert_sql, query_data)
            db.commit()
            print("success")
        except Exception as e:
            db.rollback()
            print(e)
            return e

        cursor.close()
        db.close()


if __name__ == '__main__':
    im = ImportDailyAndOvertimeRelatedData()
    im.import_overtime_form('dukang_attendance_dktest2', 743464931646504960, 743464931646504964, '2020-09-01 00:00:00',
                            '2020-09-30 00:00:00')
