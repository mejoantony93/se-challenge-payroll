"""Holds database models."""

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class ReportsUploaded(Base):
    __tablename__ = 'reports_uploaded'

    id = Column(Integer, primary_key=True, nullable=False)
    report_id = Column(Integer, nullable=False, unique=True)


class JobGroup(Base):
    __tablename__ = 'job_group'

    id = Column(Integer, primary_key=True, nullable=False)
    group_name = Column(String(1), nullable=False, unique=True)


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, nullable=False)
    fk_job_group = Column(Integer, ForeignKey(JobGroup.id), nullable=False)
    employee_id = Column(Integer, nullable=False, unique=True)

    job_group = relationship('JobGroup', foreign_keys='Employee.fk_job_group')


class WorkLog(Base):
    __tablename__ = 'work_log'

    id = Column(Integer, primary_key=True, nullable=False)
    fk_employee = Column(Integer, ForeignKey(Employee.id), nullable=False)
    hours = Column(Float, nullable=False)
    work_date = Column(Date, nullable=False)

    employee = relationship('Employee', foreign_keys='WorkLog.fk_employee')
