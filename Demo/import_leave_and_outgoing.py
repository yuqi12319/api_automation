# @Name:import_leave_and_outgoing.py
# @Author:Noah
# @Time:2020/9/10 2:55 下午

from Common.snowflake import Generator

from Common.operation_mysql import *
import pymysql
from Demo.mysql_util import get_employee_ids
from datetime import datetime, timedelta


class ImportLeaveAndOuting():
    config = {
        "host": "rm-uf6p31b6r5763b09wko.mysql.rds.aliyuncs.com",
        "user": "iac_dev",
        "password": "B1p02017",
    }

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

    # 批量添加外出记录
    def add_outgoing_into_db(self, database, attendance_group_id, begin_date, end_date ):
        query_data_outgoing = []
        query_data_outgoing_first = []
        query_data_outgoing_second = []
        id_outgoing_generator = Generator()
        id_outgoing_first_generator = Generator()
        id_outgoing_second_generator = Generator()
        employee_ids = get_employee_ids('dukang_attendance_dktest2', attendance_group_id)
        current_date = begin_date

        for employee_id in employee_ids:
            while current_date <= end_date:
                id_outgoing = int(id_outgoing_generator.generate())
                id_outgoing_first = int(id_outgoing_first_generator.generate())
                id_outgoing_second = int(id_outgoing_second_generator.generate())
                begin_date = self.time_shifter(current_date, 19, 'h')
                date = begin_date
                end_date = self.time_shifter(begin_date, 2, 'h')
                created_time = (datetime.strptime(current_date, self.date_format) - timedelta(days=1)).strftime(
                    self.date_format)
                updated_time = datetime.today().strftime(self.date_format)


                query_data_outgoing.append(
                    (id_outgoing, employee_id, attendance_group_id, begin_date, end_date, created_time, updated_time)
                )
                query_data_outgoing_first.append(
                    (id_outgoing_first, id_outgoing, employee_id, date, created_time, updated_time)
                )
                query_data_outgoing_second.append(
                    (id_outgoing_second, id_outgoing, employee_id, date, created_time, updated_time)
                )

                current_date = self.time_shifter(current_date, 1, 'd')
            current_date = begin_date

        for data in query_data_outgoing:
            print('正在拼接外出数据...\n', data)

        insert_outgoing_sql = "INSERT into outgoing_form(id, employee_id, outgoing_unit, attendance_group_id," \
                                " attendance_group_type, begin_date, begin_date_half_day, " \
                                "end_date, end_date_half_day, duration, status, deleted,created_time, updated_time) " \
                                "VALUES (%s, %s, 'BYDAY', %s, 'FIXED', %s, 'FIRSTHALF', %s, 'SECONDHALF', 1.0, 'AGREED', 0, %s, %s)"
        insert_outgoing_first_sql = "INSERT into employee_outgoing_detail(id, outgoing_form_id, employee_id, " \
                                    "date, date_half_day, created_time, updated_time)VALUES (%s, %s, %s, 'FIRSTHALF', %s, %s, %s)"
        insert_outgoing_second_sql = "INSERT into employee_outgoing_detail(id, outgoing_form_id, employee_id, " \
                                    "date, date_half_day, created_time, updated_time)VALUES (%s, %s, %s, 'SECONDHALF', %s, %s, %s)"


        db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
                             database=database, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.executemany(insert_outgoing_sql, query_data_outgoing)
            cursor.executemany(insert_outgoing_first_sql, query_data_outgoing_first)
            cursor.executemany(insert_outgoing_second_sql, query_data_outgoing_second)
            db.commit()
            print("插入外出数据成功！")
        except Exception as e:
            db.rollback()
            print(e)
            return e

        cursor.close()
        db.close()

    # 批量添加休假记录
    def add_leave_into_db(self, database, attendance_group_id, begin_date, end_date ):
        query_data_leave = []
        query_data_leave_first = []
        query_data_leave_second = []
        id_leave_generator = Generator()
        id_leave_first_generator = Generator()
        id_leave_second_generator = Generator()
        employee_ids = get_employee_ids('dukang_attendance_dktest2', attendance_group_id)
        current_date = begin_date

        for employee_id in employee_ids:
            while current_date <= end_date:
                id_leave = int(id_leave_generator.generate())
                id_leave_first = int(id_leave_first_generator.generate())
                id_leave_second = int(id_leave_second_generator.generate())
                begin_date = self.time_shifter(current_date, 19, 'h')
                date = begin_date
                end_date = self.time_shifter(begin_date, 2, 'h')
                created_time = (datetime.strptime(current_date, self.date_format) - timedelta(days=1)).strftime(
                    self.date_format)
                updated_time = datetime.today().strftime(self.date_format)

                query_data_leave.append(
                    (id_leave, employee_id, attendance_group_id, begin_date, end_date, created_time, updated_time)
                )
                query_data_leave_first.append(
                    (id_leave_first, id_leave, employee_id, date, created_time, updated_time)
                )
                query_data_leave_second.append(
                    (id_leave_second, id_leave, employee_id, date, created_time, updated_time)
                )

                current_date = self.time_shifter(current_date, 1, 'd')
            current_date = begin_date

            for data in query_data_leave:
                print('正在拼接休假数据...\n', data)

        insert_leave_sql = "INSERT into leave_form (id, employee_id, leave_type, leave_unit, attendance_group_id, " \
                           "attendance_group_type, day_conversion_hours, begin_date, begin_date_half_day, " \
                           "end_date, end_date_half_day, duration, status, deleted,created_time, updated_time)  " \
                            "VALUES (%s, %s, 'COMPASSIONATE_LEAVE', 'BYDAY', %s, 'FIXED', 8, %s, 'FIRSTHALF'," \
                           "%s, 'SECONDHALF', 1.0, 'AGREED', 0, %s, %s)"
        insert_leave_first_sql = "INSERT into employee_leave_detail(id, leave_form_id, employee_id, type, date, " \
                                     "date_half_day, created_time, updated_time) " \
                                     "VALUES(%s, %s, %s, 'COMPASSIONATE_LEAVE', %s, 'FIRSTHALF', %s, %s)"
        insert_leave_second_sql = "INSERT into employee_leave_detail(id, leave_form_id, employee_id, type, date, " \
                                     "date_half_day, created_time, updated_time) " \
                                     "VALUES(%s, %s, %s, 'COMPASSIONATE_LEAVE', %s, 'SECONDHALF', %s, %s)"

        db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
                             database=database, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.executemany(insert_leave_sql, query_data_leave)
            cursor.executemany(insert_leave_first_sql, query_data_leave_first)
            cursor.executemany(insert_leave_second_sql, query_data_leave_second)
            db.commit()
            print("插入休假数据成功！")
        except Exception as e:
            db.rollback()
            print(e)
            return e

        cursor.close()
        db.close()




if __name__ == '__main__':
    show = ImportLeaveAndOuting()
    show.add_leave_into_db('dukang_leave_dktest2', 756895524799381504, '2020-09-01 00:00:00', '2020-09-30 00:00:00')
    show.add_outgoing_into_db('dukang_leave_dktest2', 756895524799381504, '2020-09-01 00:00:00', '2020-09-30 00:00:00')