from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required

grades_bp = Blueprint("grades_bp", __name__)



# GRADE SUBMISSION
@grades_bp.route("/grades", methods=["POST"])
@token_required
def grade_submission(current_user):

    data = request.json

    submission_id = data.get("submission_id")
    grade = data.get("grade")
    feedback = data.get("feedback")

    if not submission_id or grade is None:
        return jsonify({
            "message": "Missing required fields"
        }), 400

    lecturer_id = current_user["user_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO grades
            (submission_id, lecturer_id, grade, feedback)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            submission_id,
            lecturer_id,
            grade,
            feedback
        ))

        grade_id = cur.fetchone()[0]

        conn.commit()

        return jsonify({
            "message": "Submission graded successfully",
            "grade_id": grade_id,
            "data": {
                "submission_id": submission_id,
                "lecturer_id": lecturer_id,
                "grade": grade,
                "feedback": feedback
            }
        }), 201

    except Exception as e:

        conn.rollback()

        return jsonify({
            "message": "Failed to grade submission",
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()
