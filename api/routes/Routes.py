from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import time, datetime, timedelta, date as dt_date
import pandas as pd
from fastapi.responses import FileResponse
import google.generativeai as genai
import os

from config.Database import DataBase
from models.Models import Employee, Attendance, ShiftTiming

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# Configure Gemini AI
genai.configure(api_key="AIzaSyC3OC_2xHT0gOJWlFxnoRL7NYxwzV5QAwo")

def get_db():
    db = DataBase.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.get("/analysis")
def analyze_attendance(
    start_date: dt_date = Query(..., description="Week start date (YYYY-MM-DD)"),
    end_date: dt_date = Query(..., description="Week end date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    results = {
        "latecomers": [],
        "early_comers": [],
        "overtime": [],
        "missing_checkout": []
    }

    # ✅ filter by date range
    records = (
        db.query(Attendance, Employee, ShiftTiming)
        .join(Employee, Attendance.employee_id == Employee.employee_id)
        .join(ShiftTiming, Attendance.shift_id == ShiftTiming.shift_id)
        .filter(Attendance.attendance_date >= start_date)
        .filter(Attendance.attendance_date <= end_date)
        .order_by(Attendance.attendance_date, Employee.employee_name, Attendance.actions)
        .all()
    )

    # --- (rest of your logic stays same) ---
    data = []
    late_count = early_count = overtime_count = missing_checkout_count = 0
    attendance_map = {}

    for attendance, employee, shift in records:
        # convert action_time to time
        action_time = None
        if attendance.action_time:
            if isinstance(attendance.action_time, timedelta):
                total_seconds = int(attendance.action_time.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                action_time = time(hour=hours, minute=minutes, second=seconds)
            elif isinstance(attendance.action_time, time):
                action_time = attendance.action_time
            else:
                action_time = str(attendance.action_time)

        row = {
            "Date": attendance.attendance_date,
            "Employee": employee.employee_name,
            "Employee No": employee.employee_no,
            "Shift": shift.shift_name,
            "Shift Start": shift.start_time,
            "Shift End": shift.end_time,
            "Action": attendance.actions,
            "Action Time": action_time,
        }
        data.append(row)

        # map employee attendance
        key = (employee.employee_id, attendance.attendance_date)
        if key not in attendance_map:
            attendance_map[key] = {"check_in": None, "check_out": None}

        if attendance.actions.lower() == "check-in":
            attendance_map[key]["check_in"] = action_time
            if action_time > shift.start_time:
                late_count += 1
                results["latecomers"].append({
                    "Employee": employee.employee_name,
                    "Date": attendance.attendance_date,
                    "In-Time": str(action_time),
                    "Shift Start": str(shift.start_time)
                })
            elif action_time < shift.start_time:
                early_count += 1
                results["early_comers"].append({
                    "Employee": employee.employee_name,
                    "Date": attendance.attendance_date,
                    "In-Time": str(action_time),
                    "Shift Start": str(shift.start_time)
                })

        elif attendance.actions.lower() == "check-out":
            attendance_map[key]["check_out"] = action_time
            if action_time > shift.end_time:
                overtime_count += 1
                results["overtime"].append({
                    "Employee": employee.employee_name,
                    "Date": attendance.attendance_date,
                    "Out-Time": str(action_time),
                    "Shift End": str(shift.end_time)
                })

    # check missing checkouts
    for (emp_id, date), status in attendance_map.items():
        if status["check_in"] and not status["check_out"]:
            missing_checkout_count += 1
            employee = db.query(Employee).filter(Employee.employee_id == emp_id).first()
            results["missing_checkout"].append({
                "Employee": employee.employee_name,
                "Date": date,
                "In-Time": str(status["check_in"]),
                "Note": "No check-out found"
            })

    return {
        "counts": {
            "late_comers_count": late_count,
            "early_comers_count": early_count,
            "overtime_count": overtime_count,
            "missing_checkout_count": missing_checkout_count
        },
        "details": results
    }
    
    
@router.get("/weekly-average")
def get_weekly_average(
    start_date: str = Query(..., description="Week start date in YYYY-MM-DD"),
    end_date: str = Query(..., description="Week end date in YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    from datetime import datetime, date, time, timedelta

    # Convert to datetime.date
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Fetch attendance records within range
    records = (
        db.query(Attendance, Employee, ShiftTiming)
        .join(Employee, Attendance.employee_id == Employee.employee_id)
        .join(ShiftTiming, Attendance.shift_id == ShiftTiming.shift_id)
        .filter(Attendance.attendance_date >= start_date, Attendance.attendance_date <= end_date)
        .order_by(Attendance.employee_id, Attendance.attendance_date, Attendance.action_time)
        .all()
    )

    # Step 1: Organize check-in/check-out times
    daily_hours = {}
    for (attendance, employee, shift) in records:
        date_val = attendance.attendance_date
        time_val = attendance.action_time
        emp_id = employee.employee_id
        emp_name = employee.employee_name

        if emp_id not in daily_hours:
            daily_hours[emp_id] = {"name": emp_name, "dates": {}}

        if date_val not in daily_hours[emp_id]["dates"]:
            daily_hours[emp_id]["dates"][date_val] = {"check_in": None, "check_out": None}

        if attendance.actions.lower() == "check-in":
            daily_hours[emp_id]["dates"][date_val]["check_in"] = time_val
        elif attendance.actions.lower() == "check-out":
            daily_hours[emp_id]["dates"][date_val]["check_out"] = time_val

    # Step 2: Calculate worked hours per day
    work_data = []
    for emp_id, emp_info in daily_hours.items():
        for date_val, times in emp_info["dates"].items():
            check_in, check_out = times["check_in"], times["check_out"]

            if check_in and check_out:
                # Normalize check_in and check_out
                if isinstance(check_in, timedelta):
                    check_in = (datetime.min + check_in).time()
                if isinstance(check_out, timedelta):
                    check_out = (datetime.min + check_out).time()

                hours = (
                    datetime.combine(date_val, check_out) -
                    datetime.combine(date_val, check_in)
                ).total_seconds() / 3600

                work_data.append({
                    "employee_id": emp_id,
                    "employee_name": emp_info["name"],
                    "date": date_val,
                    "hours": round(hours, 2)
                })

    # Step 3: Convert to DataFrame
    df = pd.DataFrame(work_data)

    if df.empty:
        return {"start_date": str(start_date), "end_date": str(end_date), "employees": []}

    # Step 4: Group by employee
    weekly_summary = (
        df.groupby(["employee_id", "employee_name"])["hours"]
        .agg(total_hours="sum", avg_hours="mean")
        .reset_index()
    )

    # Round numbers for readability
    weekly_summary["total_hours"] = weekly_summary["total_hours"].round(2)
    weekly_summary["avg_hours"] = weekly_summary["avg_hours"].round(2)

    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "employees": weekly_summary.to_dict(orient="records")
    }

@router.get("/top-performers")
def top_performers(
    start_date: dt_date = Query(..., description="Week start date (YYYY-MM-DD)"),
    end_date: dt_date = Query(..., description="Week end date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    # Fetch records within the date range
    records = (
        db.query(Attendance, Employee, ShiftTiming)
        .join(Employee, Attendance.employee_id == Employee.employee_id)
        .join(ShiftTiming, Attendance.shift_id == ShiftTiming.shift_id)
        .filter(Attendance.attendance_date.between(start_date, end_date))
        .order_by(Attendance.attendance_date)
        .all()
    )

    # Track punctuality per employee
    punctuality_map = {}

    for attendance, employee, shift in records:
        if attendance.actions.lower() == "check-in" and attendance.action_time:
            # Convert timedelta -> time if needed
            action_time = None
            if isinstance(attendance.action_time, timedelta):
                total_seconds = int(attendance.action_time.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                action_time = time(hour=hours, minute=minutes, second=seconds)
            elif isinstance(attendance.action_time, time):
                action_time = attendance.action_time
            else:
                continue

            # Check punctuality
            if action_time <= shift.start_time:  
                if employee.employee_id not in punctuality_map:
                    punctuality_map[employee.employee_id] = {
                        "Employee": employee.employee_name,
                        "Employee No": employee.employee_no,
                        "Punctual Days": 0
                    }
                punctuality_map[employee.employee_id]["Punctual Days"] += 1

    # Sort by punctual days and pick top 5
    top_punctual = sorted(
        punctuality_map.values(),
        key=lambda x: x["Punctual Days"],
        reverse=True
    )[:5]

    return {
        "week_start": str(start_date),
        "week_end": str(end_date),
        "top_5_punctual_employees": top_punctual
    }
    
@router.get("/top-punctual")
def get_top_punctual(
    start_date: str = Query(..., description="Week start date in YYYY-MM-DD"),
    end_date: str = Query(..., description="Week end date in YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    # Convert to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Fetch records
    records = (
        db.query(Attendance, Employee, ShiftTiming)
        .join(Employee, Attendance.employee_id == Employee.employee_id)
        .join(ShiftTiming, Attendance.shift_id == ShiftTiming.shift_id)
        .filter(Attendance.attendance_date >= start_date, Attendance.attendance_date <= end_date)
        .order_by(Attendance.employee_id, Attendance.attendance_date, Attendance.action_time)
        .all()
    )

    # Step 1: Organize daily attendance
    punctuality_data = {}
    for (attendance, employee, shift) in records:
        emp_id = employee.employee_id
        emp_name = employee.employee_name
        date = attendance.attendance_date

        if emp_id not in punctuality_data:
            punctuality_data[emp_id] = {"name": emp_name, "punctual_days": 0, "total_days": 0}

        # Mark check-in punctuality
        if attendance.actions.lower() == "check-in":
            punctuality_data[emp_id]["total_days"] += 1
            attendance_time = (datetime.min + attendance.action_time).time()
            if attendance_time <= shift.start_time:  # On time
                punctuality_data[emp_id]["punctual_days"] += 1

    # Step 2: Convert to DataFrame
    data = [
        {
            "employee_id": emp_id,
            "employee_name": info["name"],
            "punctual_days": info["punctual_days"],
            "total_days": info["total_days"],
            "punctuality_rate": round((info["punctual_days"] / info["total_days"]) * 100, 2) if info["total_days"] else 0
        }
        for emp_id, info in punctuality_data.items()
    ]

    df = pd.DataFrame(data)
    if df.empty:
        return {"message": "No attendance records found for the given week"}

    # Step 3: Get Top 5 Punctual Employees
    top_employees = df.sort_values(by="punctuality_rate", ascending=False).head(5).to_dict(orient="records")

    # Step 4: Use Gemini to analyze top employees
    model = genai.GenerativeModel("gemini-2.0-flash")
    summary_prompt = f"""
    I have attendance punctuality data for employees between {start_date} and {end_date}.
    The top punctual employees are:
    {top_employees}

    For each of these employees, please provide:
    1. Pros: Strengths or positive habits that make them punctual.
    2. Cons: Possible areas of improvement.
    3. Reason they are among the top punctual employees.

    Provide the analysis in a professional, clear, and motivating way.
    """
    ai_response = model.generate_content(summary_prompt)

    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "top_punctual_employees": top_employees,
        "ai_analysis": ai_response.text
    }
