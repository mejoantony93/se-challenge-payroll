"""Performs logical operations."""

import re
from db_connect import session
from models import ReportsUploaded, WorkLog, Employee


def existing_report_check(report_id):
    """Checks if report id exist in database."""

    existing_check = session.query(ReportsUploaded).filter(
        ReportsUploaded.report_id == report_id).first()
    return bool(existing_check)


def verify_filename(filename):
    """Verifies file name against the specified pattern."""

    pattern = re.compile('time-report-\\d+.csv')
    return bool(pattern.match(filename))


def process_worklog():
    """Creates an intermediate json in the following format:
        {
          "Employee ID": {
            "group": "Job Group",
            "Tuple in the format (month, year)": {
              "pay_1": "Sum of hours worked in first half of the month",
              "pay_2": "Sum of hours worked in second half of the month"
            },
            "Tuple in the format (another_month, year)": {
              "pay_1": "Sum of hours worked in first half of the month",
              "pay_2": "Sum of hours worked in second half of the month"
            }
          },
          "Another Employee ID": {
            "group": "Job Group",
            "Tuple in the format (month, year)": {
              "pay_1": "Sum of hours worked in first half of the month",
              "pay_2": "Sum of hours worked in second half of the month"
            },
            "Tuple in the format (another_month, year)": {
              "pay_1": "Sum of hours worked in first half of the month",
              "pay_2": "Sum of hours worked in second half of the month"
            }
          }
        }
    """

    intermediate_json = {}
    work_logs = session.query(WorkLog).join(WorkLog.employee).order_by(
        Employee.employee_id
    ).all()

    for log in work_logs:
        month_key = (log.work_date.month, log.work_date.year)
        emp_id = log.employee.employee_id
        group_name = log.employee.job_group.group_name

        if emp_id not in intermediate_json:
            intermediate_json[emp_id] = {"group": group_name}
        if month_key not in intermediate_json[emp_id]:
            intermediate_json[emp_id][month_key] = {'pay_1': 0, 'pay_2': 0}
        if log.work_date.day <= 15:
            intermediate_json[emp_id][month_key]['pay_1'] += log.hours
        else:
            intermediate_json[emp_id][month_key]['pay_2'] += log.hours

    return intermediate_json
