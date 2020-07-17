# coding:utf-8
# Name:operation_mysql.py
# Author:qi.yu
# Time:2020/
# 6/30 4:20 下午

import pymysql

mysqlDict = {
    "host": "rm-uf6p31b6r5763b09wko.mysql.rds.aliyuncs.com",
    "user": "iac_dev",
    "password": "B1p02017",
}


def mysql_operate_select_fetchall(database, select_sql=None):
    db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
                         database=database, charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if select_sql is not None:
        try:
            cursor.execute(select_sql)
            data = cursor.fetchall()
        except Exception as e:
            print("Error:unable to fetch data")
            return e
    else:
        pass

    cursor.close()
    db.close()
    return data


def mysql_operate_select_fetchone(database, select_sql=None):
    db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
                         database=database, charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if select_sql is not None:
        try:
            cursor.execute(select_sql)
            data = cursor.fetchone()
        except Exception as e:
            print("Error:unable to fetch data")
            return e
    else:
        pass

    cursor.close()
    db.close()
    return data


def mysql_operate_insert_update_delete(database, insert_sql=None, update_sql=None, delete_sql=None):
    db = pymysql.connect(host=mysqlDict['host'], port=3306, user=mysqlDict['user'], password=mysqlDict['password'],
                         database=database, charset='utf8')
    cursor = db.cursor()

    if insert_sql is not None:
        try:
            cursor.execute(insert_sql)
            db.commit()
        except Exception as e:
            db.rollback()
            return e
    else:
        pass

    if update_sql is not None:
        try:
            cursor.execute(update_sql)
            db.commit()
        except Exception as e:
            db.rollback()
            return e
    else:
        pass

    if delete_sql is not None:
        try:
            cursor.execute(delete_sql)
            db.commit()
        except Exception as e:
            db.rollback()
            return e
    else:
        pass

    cursor.close()
    db.close()
