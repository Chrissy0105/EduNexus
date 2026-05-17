from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required

courses_bp = Blueprint("courses_bp", __name__)


# GET COURSES (PUBLIC)
@courses_bp.route("/", methods=["GET"])
def get_courses():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(courses), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# CREATE COURSE (ADMIN ONLY)
@courses_bp.route("/", methods=["POST"])
@token_required
def create_course(current_user):
    try:
        if current_user["role"] != "admin":
            return jsonify({"message": "Admin only"}), 401

        data = request.json

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO courses (course_code, course_name, description, lecturer_id)
            VALUES (%s, %s, %s, %s)
        """, (
            data["course_code"],
            data["course_name"],
            data["description"],
            data["lecturer_id"]
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Course created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ENROLL COURSE (STUDENT ONLY)
@courses_bp.route("/enroll", methods=["POST"])
@token_required
def enroll_course(current_user):
    try:
        if current_user["role"] != "student":
            return jsonify({"message": "Students only"}), 401

        data = request.json

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO enrollments (user_id, course_id)
            VALUES (%s, %s)
        """, (current_user["user_id"], data["course_id"]))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Enrolled successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500