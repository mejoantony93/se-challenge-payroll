# Wave Software Development Challenge

This is a containerized application. You need to install `docker` and
`docker-compose` in order to deploy this application.

## Steps to run
1. Install `docker`.
2. Install `docker-compose`.
3. Install `PostgreSQL` database.
4. Create a database for the project.
5. Create tables `reports_uploaded`, `job_group`, `employee`, `work_log`
based on the schema in `models.py` file.
6. Update environment variables in the `docker-compose.yml` file
   - `DB_NAME`: Name of the database
   - `DB_USER`: Username of the database
   - `DB_PASS`: Password of the database
   - `DB_HOST`: IP of the database host system
   - `DB_PORT`: Port on which the database is running
7. Run the command `docker-compose up` in your terminal from the project
folder.
8. Now you can access the end points at
   - `127.0.0.1:7000/upload_report` - Endpoint for uploading a report file.
     - `file` - form-data file parameter to upload the report
   - `127.0.0.1:7100/payroll_report` - Endpoint for retrieving payroll report.

## Answers to the Questions
1. How did I test that implementation was correct?
   - I used Postman API platform to test and verify my APIs.
   - PyCharm IDE and its debug tools for development.
2. What would I change, for a production environment?
   - I would serve flask over any WSGI server like waitress for a production
environment.
3. Compromises I made due to time constraints.
   - I prefer FastAPI over flask for this application, but I am not that
   familiar with it so I need some time to research and implement. Thus, since
   there is a time constraint, I used flask framework.
