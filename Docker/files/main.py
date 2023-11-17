"""The main controller for apis."""

from csv import reader
from pathlib import Path
import io
import datetime
import calendar
import flask
from db_connect import session
from models import ReportsUploaded, JobGroup, Employee, WorkLog
from utilities import existing_report_check, verify_filename, process_worklog

api = flask.Flask(__name__)

GROUP_RATE = {'A': 20, 'B': 30}


@api.route('/upload_report', methods=['POST'])
def api_upload_report():
    """Endpoint for uploading a report file."""

    try:
        data_file = flask.request.files['file']
        filename = Path(data_file.filename)

        # Check for filename validity
        if not verify_filename(str(filename)):
            return flask.jsonify({
                'status': 'Failure',
                'message': 'Wrong file name pattern.'
            }), 403

        # Existing report check
        report_id = int(filename.stem.split('-')[-1])
        if existing_report_check(report_id):
            return flask.jsonify({
                'status': 'Failure',
                'message': 'This report is already uploaded.'
            }), 403

        # Creating report id record
        report = ReportsUploaded(report_id=report_id)
        session.add(report)

        csv_data = reader(io.StringIO(data_file.stream.read().decode("UTF8")))

        # Omitting the header
        next(csv_data)

        # Reading each line in the csv
        for line in csv_data:

            date = datetime.datetime.strptime(line[0], "%d/%m/%Y").date()

            # Checking if the job group already exist otherwise creating it
            existing_job_grp = session.query(JobGroup).filter(
                JobGroup.group_name == line[3]).first()
            if existing_job_grp:
                job_group_id = existing_job_grp.id
            else:
                new_job_grp = JobGroup(group_name=line[3])
                session.add(new_job_grp)
                session.flush()
                job_group_id = new_job_grp.id

            # Checking if the employee already exist otherwise creating it
            existing_emp = session.query(Employee).filter(
                Employee.employee_id == int(line[2])).first()
            if existing_emp:
                emp_id = existing_emp.id
            else:
                new_employee = Employee(
                    fk_job_group=job_group_id,
                    employee_id=int(line[2])
                )
                session.add(new_employee)
                session.flush()
                emp_id = new_employee.id

            # Creating the work log record based on the params
            new_work_log = WorkLog(
                fk_employee=emp_id,
                hours=float(line[1]),
                work_date=date
            )
            session.add(new_work_log)

    except Exception as error:
        # Rolling back any db changes if exception occurs
        session.rollback()
        return flask.jsonify(error={'error': str(error)}), 400

    else:
        # Finally committing all the changes to the database
        session.commit()
        return flask.jsonify({'status': 'Success'}), 200

    finally:
        session.close()


@api.route('/payroll_report', methods=['GET'])
def api_payroll_report():
    """Endpoint for retrieving payroll report."""

    try:
        report_data = {"payrollReport": {"employeeReports": []}}

        # Creates an intermediate json for processing
        intermediate_json = process_worklog()

        for key, value in intermediate_json.items():
            group = value.pop('group')

            for k, val in value.items():

                # Calculates pay amount per period based on job group
                amount_1 = GROUP_RATE[group] * val['pay_1']
                amount_2 = GROUP_RATE[group] * val['pay_2']

                # Month and year is fetched from key tuple
                month, year = k

                # Creates output record for the month, first pay period
                if amount_1 > 0:
                    new_record = {
                        "employeeId": str(key),
                        "payPeriod": {
                            "startDate": str(datetime.date(year, month, 1)),
                            "endDate": str(datetime.date(year, month, 15))
                        },
                        "amountPaid": f'${amount_1:.2f}'
                    }
                    report_data['payrollReport']['employeeReports'].append(
                        new_record
                    )

                # Creates output record for the month, second pay period
                if amount_2 > 0:
                    end_date = datetime.date(
                        year, month, calendar.monthrange(year, month)[-1]
                    )
                    new_record = {
                        "employeeId": str(key),
                        "payPeriod": {
                            "startDate": str(datetime.date(year, month, 16)),
                            "endDate": str(end_date)
                        },
                        "amountPaid": f'${amount_2:.2f}'
                    }
                    report_data['payrollReport']['employeeReports'].append(
                        new_record
                    )

        return flask.jsonify(report_data), 200
    except Exception as error:
        return flask.jsonify(
            error={'error': str(error)}), 400
