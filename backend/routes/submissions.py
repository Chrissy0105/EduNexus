from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required

submissions_bp = Blueprint("submissions_bp", __name__)


# =========================================
# SUBMIT ASSIGNMENT
# =========================================
@submissions_bp.route("/submissions", methods=["POST"])
@token_required
def submit_assignment(current_user):

    data = request.json

    assignment_id = data.get("assignment_id")
    submission_text = data.get("submission_text")

    if not assignment_id or not submission_text:
        return jsonify({
            "message": "Missing required fields"
        }), 400

    student_id = current_user["user_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO submissions
            (assignment_id, student_id, submission_text)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (
            assignment_id,
            student_id,
            submission_text
        ))

        submission_id = cur.fetchone()[0]

        conn.commit()

        return jsonify({
            "message": "Assignment submitted successfully",
            "submission_id": submission_id,
            "data": {
                "assignment_id": assignment_id,
                "student_id": student_id,
                "submission_text": submission_text
            }
        }), 201

    except Exception as e:

        conn.rollback()

        return jsonify({
            "message": "Failed to submit assignment",
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()