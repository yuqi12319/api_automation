# coding:utf-8
# Name:operation_mysql.py
# Author:qi.yu
# Time:2020/6/29 5:59 下午

import pymysql
import requests
from Common.operation_random import *
from Common.operation_mysql import *
import datetime


def login():
    url = 'http://dktest2-workio.bipocloud.com/services/dukang-user/login'
    data = {
        'areaCode': '86',
        'clientId': 'gardenia',
        'password': '12345678',
        'username': '18373280066'
    }
    res = requests.post(url=url,json=data,verify=False)
    return res

#添加薪资项目
def add_salaryproject():
    access_token = login().json()['data']['accessToken']
    url = 'http://dktest2-workio.bipocloud.com/services/dukang-payroll/payrollItem'
    select_sql = "SELECT b.calculation_type,b.co_org_id,a.content,b.cycle_type,a.editor_components,b.`name`,b.tax_mode,b.tax_type,b.type,a.expression FROM payroll_item_formula AS a INNER JOIN payroll_item AS b ON b.id = a.payroll_item_id WHERE a.content NOT IN ('') AND b.`name` NOT IN ('基本工资','工作日加班费','休息日加班费','法定假日加班费','事假','病假','缺勤') GROUP BY a.content ORDER BY b.created_time DESC LIMIT 300"
    sqls = mysql_operate_select_fetchall('dukang_payroll_dktest2',select_sql=select_sql)

    for sql in sqls:
        data = {
            'calculationType': sql[0],
            'coOrgId': '727184158689853440',
            'code': None,
            'content': sql[2],
            'cycleType': sql[3],
            'editorComponents': sql[4],
            'name': sql[5],
            'payrollItemId': None,
            'remark': None,
            'taxMode': sql[6],
            'taxType': sql[7],
            'type': sql[8],
            'value': sql[9]
        }
        headers = {
            'content-type':'application/json;charset=UTF-8',
            'x-companyid':'727184158689853440',
            'x-dk-token':access_token,
            'x-employeeid':'727184158668881920',
            'x-language':'zh'
        }
        res = requests.post(url=url,json=data,headers=headers,verify=False)
        print(res.json())

#给员工补充身份证信息
def update_idcard():
    # select_employee = "SELECT id FROM employee WHERE co_org_id = '727184158689853440' AND display_name NOT IN ('Administrator')"
    select_employee = "SELECT employee_id as id FROM employee_certificate WHERE type IS NULL AND employee_id in (SELECT id FROM employee WHERE co_org_id = '727184158689853440' AND display_name NOT IN ('Administrator')) "
    employee_ids = mysql_operate_select_fetchall('bipo_lite_dktest2',select_sql=select_employee)
    for employee_id in employee_ids:
        id_card = random_idcard()
        update_sql = "UPDATE employee_certificate SET type = 'IDCard',number="+str(id_card)+",photo='[]' WHERE employee_id = "+str(employee_id['id'])
        mysql_operate_insert_update_delete('bipo_lite_dktest2',update_sql=update_sql)

#关联员工和薪资项目
def relevance_employee_salaryproject():
    accesstoken = login().json()['data']['accessToken']
    # 获取薪资项目列表（薪资项目id，公司id）
    payrollItemId_sql = "SELECT id,co_org_id FROM payroll_item WHERE co_org_id = '727184158689853440'"
    payrollItemId_datas = mysql_operate_select_fetchall('dukang_payroll_dktest2',select_sql=payrollItemId_sql)

    payrollItemList = []
    for payrollItemId_data in payrollItemId_datas:
        a = {
                "allowance": {"factorAllowanceList": []},
                "factorAllowanceList": "[]",
                "currency": "CNY",
                "endDate": None,
                "payrollItemId": str(payrollItemId_data['id']),
                "startDate": 1577808000000
            }
        payrollItemList.append(a)

    #获取需要关联的员工信息(员工id，公司ID，身份证)
    relevance_employee_sql = "SELECT a.id,a.co_org_id,b.number FROM employee a INNER JOIN employee_certificate b ON a.id = b.employee_id WHERE a.co_org_id = '727184158689853440' AND a.id NOT IN (SELECT DISTINCT employee_id FROM dukang_payroll_dktest2.employee_payroll_item_map WHERE co_org_id = '727184158689853440')"
    relevance_employee_datas = mysql_operate_select_fetchall('bipo_lite_dktest2',relevance_employee_sql)

    i = 0
    for relevance_employee_data in relevance_employee_datas:
        url = "http://dktest2-workio.bipocloud.com/services/dukang-payroll/employee/salary?employeeId="+str(relevance_employee_data['id'])
        data = {
            "baseSalary":[
                {
                "currency":"CNY",               #固定工资货币类型
                "money":"10000.00",             #固定工资金额
                "remark":"",                    #固定工资备注
                "salaryType":"tax_before",      #固定工资工资类型
                "startDate":1577808000000,      #固定工资开始时间
                "taxMode": "WagesAndSalaries"   #固定工资计税类型
                }
            ],
            "chineseFlag":True,     #是否中国居民
            "coOrgId":str(relevance_employee_data['co_org_id']), #公司id
            "departmentId": "",     #报送部门id
            "identityNo": str(relevance_employee_data['number']), #身份证
            "itEntityId": "",   #个税主体id
            "paygroupId": "727184760819941376", #帐套id   需改动
            "payrollItemList":payrollItemList   #薪资项目列表
        }
        headers = {
            "x-companyid":str(relevance_employee_data['co_org_id']),
            "x-dk-token":accesstoken,
            "x-employeeid":"727184158668881920",  #管理员id 需改动
            "x-language":"zh"
        }
        res = requests.put(url=url,json=data,headers=headers,verify=False)


        if res.status_code == 200:
            i = i+1
            print(i)
        else:
            pass

# def relevance_employee_salaryproject():
#     accessToken = login().json()['data']['accessToken']
#     url = "http://dktest2-workio.bipocloud.com/services/dukang-payroll/addEmployeePayrollItem"
#     headers = {
#         "x-dk-token":accessToken
#     }
#     data = {
#         "coOrgId":"724563241753116672"
#     }
#     res = requests.get(url=url,json=data,headers=headers,verify=False)
#     print(res.json())

#增加考勤信息
def add_daily_attendance():
    earliest_daily_select_sql = "SELECT clock_date FROM daily_attendance WHERE emplpoyee_id = '724581135954214912' ORDER BY clock_date ASC LIMIT 1"
    earliest_daily_data = mysql_operate_select_fetchone("dukang_attendance_dktest2",earliest_daily_select_sql)
    if int(earliest_daily_data['clock_date'].strftime('%d')) >15:
        for i in range(int(earliest_daily_data['clock_date'].strftime('%d'))-1):
            id = snowflake()
            daily_insert_sql = "INSERT INTO `dukang_attendance_dktest2`.`daily_attendance`(`id`, `co_org_id`, `emplpoyee_id`, `clock_date`, `clock_in`, `clock_out`, `attendance_group_id`, `attendance_group_type`, `shift_id`, `shift_type`, `shift_name`, `short_name`, `to_work_time`, `off_work_time`, `accept_towork_late_duration`, `accept_leave_earlier_duration`, `am_leave_towork_time`, `pm_leave_offwork_time`, `shift_rest_time`, `shift_off_work_after_scope_time`, `shift_off_work_before_scope_time`, `shift_to_work_after_scope_time`, `shift_to_work_before_scope_time`, `holiday_plan_id`, `holiday_name`, `clock_switch`, `time_count_to`, `time_count_off`, `min_duration`, `max_duration`, `workday_compensation`, `restday_compensation`, `holiday_compensation`, `holiday_plan_name`, `lateness_minutes`, `leaveearly_minutes`, `ot_actual_minutes_work`, `ot_actual_minutes_off`, `ot_actual_minutes_holiday`, `ot_authorize_minutes_work`, `ot_authorize_minutes_off`, `ot_authorize_minutes_holiday`, `first_half_leave`, `second_half_leave`, `full_leave`, `first_half_out`, `second_half_out`, `leave_duration`, `leave_duration_second`, `day_conversion_hours`, `full_out`, `absence`, `no_clock`, `late_or_early`, `status`, `created_time`, `updated_time`) VALUES ("+id+", 724563241753116672, 724581135954214912, '2020-06-"+str(i+1)+" 00:00:00', NULL, NULL, 724563244844318720, 'FIXED', 724563244844318724, 'WORK', '默认班次', NULL, 32400, 64800, 0, 0, 50400, 46800, '', 14400, 7200, 7200, 7200, 13, NULL, 1, 3600, 3600, 3600, 43200, 'ONETIMESPAY', 'OPFTIMEPAY', 'THREETIMESPAY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 'ABNORMAL', '"+str(time.strftime('%Y-%m-%d %H:%M:%S'))+"','"+str(time.strftime('%Y-%m-%d %H:%M:%S'))+"');"
            mysql_operate_insert_update_delete("dukang_attendance_dktest2",daily_insert_sql)
    else:
        for i in range(30):
            id = snowflake()
            daily_insert_sql = "INSERT INTO `dukang_attendance_dktest2`.`daily_attendance`(`id`, `co_org_id`, `emplpoyee_id`, `clock_date`, `clock_in`, `clock_out`, `attendance_group_id`, `attendance_group_type`, `shift_id`, `shift_type`, `shift_name`, `short_name`, `to_work_time`, `off_work_time`, `accept_towork_late_duration`, `accept_leave_earlier_duration`, `am_leave_towork_time`, `pm_leave_offwork_time`, `shift_rest_time`, `shift_off_work_after_scope_time`, `shift_off_work_before_scope_time`, `shift_to_work_after_scope_time`, `shift_to_work_before_scope_time`, `holiday_plan_id`, `holiday_name`, `clock_switch`, `time_count_to`, `time_count_off`, `min_duration`, `max_duration`, `workday_compensation`, `restday_compensation`, `holiday_compensation`, `holiday_plan_name`, `lateness_minutes`, `leaveearly_minutes`, `ot_actual_minutes_work`, `ot_actual_minutes_off`, `ot_actual_minutes_holiday`, `ot_authorize_minutes_work`, `ot_authorize_minutes_off`, `ot_authorize_minutes_holiday`, `first_half_leave`, `second_half_leave`, `full_leave`, `first_half_out`, `second_half_out`, `leave_duration`, `leave_duration_second`, `day_conversion_hours`, `full_out`, `absence`, `no_clock`, `late_or_early`, `status`, `created_time`, `updated_time`) VALUES ("+id+", 724563241753116672, 724581135954214912, '2020-06-"+str(i+1)+" 00:00:00', NULL, NULL, 724563244844318720, 'FIXED', 724563244844318724, 'WORK', '默认班次', NULL, 32400, 64800, 0, 0, 50400, 46800, '', 14400, 7200, 7200, 7200, 13, NULL, 1, 3600, 3600, 3600, 43200, 'ONETIMESPAY', 'OPFTIMEPAY', 'THREETIMESPAY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 'ABNORMAL', '"+str(time.strftime('%Y-%m-%d %H:%M:%S'))+"','"+str(time.strftime('%Y-%m-%d %H:%M:%S'))+"');"
            mysql_operate_insert_update_delete("dukang_attendance_dktest2",daily_insert_sql)


# add_daily_attendance()
# relevance_employee_salaryproject()
# test1()
