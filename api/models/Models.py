from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Time, Boolean, ForeignKey, TIMESTAMP, func
)
from sqlalchemy.orm import relationship
from config.Database import DataBase


class Employee(DataBase.Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_no = Column(String(15), nullable=False, unique=True)
    employee_name = Column(String(30), nullable=False)

    shift_timing_id = Column(Integer, ForeignKey("shift_timings.shift_id"), nullable=False)

    # Relationships
    shift = relationship("ShiftTiming", back_populates="employees")
    attendances = relationship("Attendance", back_populates="employee")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Attendance(DataBase.Base):
    __tablename__ = "attendance_tracking"

    attendance_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employee.employee_id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shift_timings.shift_id"), nullable=False)

    attendance_date = Column(Date, nullable=False)
    actions = Column(String(10), nullable=True)  # e.g., IN / OUT
    action_time = Column(DateTime, nullable=True)

    # Relationships
    employee = relationship("Employee", back_populates="attendances")
    shift = relationship("ShiftTiming", back_populates="attendances")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Holiday(DataBase.Base):
    __tablename__ = "company_holidays"

    holiday_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    holiday_date = Column(Date, nullable=False, unique=True)
    holiday_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Calendar(DataBase.Base):
    __tablename__ = "dim_date"

    date = Column(Date, primary_key=True, nullable=False)
    day_no = Column(Integer, nullable=True)
    day_suffix = Column(String(5), nullable=True)
    day_of_week = Column(Integer, nullable=True)
    week_no = Column(Integer, nullable=True)
    week_day_name = Column(String(30), nullable=True)
    week_day_name_short = Column(String(5), nullable=True)
    week_day_name_first_letter = Column(String(2), nullable=True)
    is_weekend = Column(Boolean, nullable=True)  # better than Integer(0/1)


class ShiftTiming(DataBase.Base):
    __tablename__ = "shift_timings"

    shift_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shift_name = Column(String(50), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_minutes = Column(Integer, nullable=True, default=0)

    # Relationships
    employees = relationship("Employee", back_populates="shift")
    attendances = relationship("Attendance", back_populates="shift")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
