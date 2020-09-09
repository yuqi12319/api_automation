# @Name:import_leave_and_outing.py
# @Author:Noah
# @Time:2020/9/8 1:35 下午

from math import floor
from random import random
from Common import snowflake
from Common.operation_mysql import *
import pymysql


class ImportLeaveAndOuting:
    config = {
        "host": "rm-uf6p31b6r5763b09wko.mysql.rds.aliyuncs.com",
        "user": "iac_dev",
        "password": "B1p02017",
    }

    # 生成随机id
    def generate_id(self):
        snow = snowflake.Generator(worker_id=floor(random() * 32))
        self.id = snow.generate()
        return str(self.id)

    # 添加请假记录和外出记录
    def add_leave_and_outgoing_into_db(self, database):
        db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
                             database=database, charset='utf8')
        cursor = db.cursor()

        # 添加请假记录
        for i in range(30):
            id_leave_form = self.generate_id()
            id_employee_leave_detail_first = self.generate_id()
            id_employee_leave_detail_second = self.generate_id()
            id_outgoing_form = self.generate_id()
            id_employee_outgoing_detail_first = self.generate_id()
            id_employee_outgoing_detail_second = self.generate_id()

            sql_leave_form = "INSERT into `leave_form` (`id`, `employee_id`, `leave_type`, `leave_unit`, " \
              "`attendance_group_id`, `attendance_group_name`, `attendance_group_type`, `day_conversion_hours`, `begin_date`, " \
              "`begin_date_half_day`, `end_date`, `end_date_half_day`, `duration`, `status`, `deleted`,`created_time`, `updated_time`)  " \
              "values " \
              "("+id_leave_form+", 748608405077229568, 'COMPASSIONATE_LEAVE', 'BYDAY', 748596799903629312, '默认考勤组', 'FIXED', " \
              "8, '2020-09-07 00:00:00', 'FIRSTHALF', '2020-09-"+str(i+1)+" 00:00:00', 'SECONDHALF', '1.0', 'AGREED', 0, '2020-09-"+str(i+1)+" 00:00:00', '2020-09-09 10:56:32')"

            # 添加请假记录，一条leave_form表里的数据，对应employee_leave_form表里的上半天和下半天两条数据
            sql_employee_leave_detail_first = "INSERT into `employee_leave_detail`(`id`, `leave_form_id`, `employee_id`, `type`, " \
                                              "`date`, `date_half_day`, `created_time`, `updated_time`)" \
                                              "values" \
                                              "(" + id_employee_leave_detail_first + ", " + id_leave_form + ", 748608405077229568, 'COMPASSIONATE_LEAVE'," \
                                                "'2020-09-"+str(i+1)+" 00:00:00', 'FIRSTHALF', '2020-09-"+str(i+1)+" 00:00:00', '2020-09-09 10:56:32')"

            sql_employee_leave_detail_second = "INSERT into `employee_leave_detail`(`id`, `leave_form_id`, `employee_id`, `type`, " \
                                               "`date`, `date_half_day`, `created_time`, `updated_time`)" \
                                               "values" \
                                               "(" + id_employee_leave_detail_second + ", " + id_leave_form + ", 748608405077229568, 'COMPASSIONATE_LEAVE'," \
                                                "'2020-09-"+str(i+1)+" 00:00:00', 'SECONDHALF', '2020-09-"+str(i+1)+" 00:00:00', '2020-09-09 10:56:32')"

            # 添加外出记录
            sql_outgoing_form = "INSERT into `outgoing_form`(`id`, `employee_id`, `outgoing_unit`, `attendance_group_id`," \
                                "`attendance_group_name`, `attendance_group_type`, `begin_date`, `begin_date_half_day`, " \
                                "`end_date`, `end_date_half_day`, `duration`, `status`, `deleted`,`created_time`, `updated_time`) " \
                                "values" \
                                "(" + id_outgoing_form + ", 748608405077229568, 'BYDAY', 748596799903629312, '默认考勤组', 'FIXED'," \
                                                         "'2020-09-"+str(i+1)+" 00:00:00', 'FIRSTHALF', '2020-09-"+str(i+1)+" 00:00:00', 'SECONDHALF', '1.0', 'AGREED', 0, '2020-09-07 00:00:00', '2020-09-09 10:56:32')"

            # 添加外出记录，一条outgoing_form表里的数据，对应employee_outgoing_detail表中的上半天和下半天两条数据
            sql_employee_outgoing_detail_first = "INSERT into `employee_outgoing_detail`(`id`, `outgoing_form_id`, `employee_id`," \
                                                 "`date`, `date_half_day`, `created_time`, `updated_time`)" \
                                                 "values" \
                                                 "(" + id_employee_outgoing_detail_first + ", " + id_outgoing_form + ", '748608405077229568'," \
                                                    "'2020-09-"+str(i+1)+" 00:00:00', 'FIRSTHALF', '2020-09-"+str(i+1)+" 00:00:00', '2020-09-09 10:56:32')"

            sql_employee_outgoing_detail_second = "INSERT into `employee_outgoing_detail`(`id`, `outgoing_form_id`, `employee_id`," \
                                                  "`date`, `date_half_day`, `created_time`, `updated_time`)" \
                                                  "values" \
                                                  "(" + id_employee_outgoing_detail_second + ", " + id_outgoing_form + ", '748608405077229568'," \
                                                    "'2020-09-"+str(i+1)+" 00:00:00', 'SECONDHALF', '2020-09-"+str(i+1)+" 00:00:00', '2020-09-09 10:56:32')"

            cursor.execute(sql_leave_form)
            cursor.execute(sql_employee_leave_detail_first)
            cursor.execute(sql_employee_leave_detail_second)
            cursor.execute(sql_outgoing_form)
            cursor.execute(sql_employee_outgoing_detail_first)
            cursor.execute(sql_employee_outgoing_detail_second)
            db.commit()

        cursor.close()
        db.close()
        print("insert成功！")






if __name__ == '__main__':
    show = ImportLeaveAndOuting()
    show.generate_id()
    show.add_leave_and_outgoing_into_db('dukang_leave_dktest2')