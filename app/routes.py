from flask import request, jsonify, render_template
from app import app
from app.models import add_student, mark_attendance, get_attendance, get_attendance_stats, get_student_attendance
from datetime import date, datetime

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register_student', methods=['POST'])
def register_student():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    student_id = add_student(name)
    mark_attendance(student_id, str(date.today()), "Present")

    return jsonify({"message": f"Attendance recorded for {name}!"})

@app.route('/mark_absent', methods=['POST'])
def mark_absent():
    data = request.get_json()
    student_id = data.get("student_id")

    if not student_id:
        return jsonify({"error": "Student ID is required"}), 400

    mark_attendance(student_id, str(date.today()), "Absent")

    return jsonify({"message": "Student marked as Absent!"})

@app.route('/get_attendance', methods=['GET'])
def fetch_attendance():
    records = get_attendance()
    return render_template("attendance.html", records=records)

@app.route('/analytics')
def analytics_page():
    return render_template("analytics.html")

@app.route('/attendance_stats', methods=['GET'])
def attendance_stats():
    start_date = request.args.get('start_date', '2023-01-01')  # Default start date
    end_date = request.args.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    student_name = request.args.get('student_name', None)  # Optional filter by student

    if student_name:
        stats = get_student_attendance(student_name, start_date, end_date)
    else:
        stats = get_attendance_stats(start_date, end_date)

    return jsonify(stats)
