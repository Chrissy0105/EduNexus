from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required

assignments_bp = Blueprint("assignments_bp", __name__)


# =========================================
# CREATE ASSIGNMENT
# =========================================
@assignments_bp.route("/assignments", methods=["POST"])
@token_required
def create_assignment(current_user):

    data = request.json

    course_id = data.get("course_id")
    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")

    if not course_id or not title or not due_date:
        return jsonify({
            "message": "Missing required fields"
        }), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO assignments
            (course_id, title, description, due_date)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            course_id,
            title,
            description,
            due_date
        ))

        assignment_id = cur.fetchone()[0]

        conn.commit()

        return jsonify({
            "message": "Assignment created",
            "assignment_id": assignment_id,
            "data": {
                "course_id": course_id,
                "title": title,
                "description": description,
                "due_date": due_date
            }
        }), 201

    except Exception as e:

        conn.rollback()

        return jsonify({
            "message": "Failed to create assignment",
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()


# =========================================
# GET COURSE ASSIGNMENTS
# =========================================
@assignments_bp.route("/courses/<int:course_id>/assignments", methods=["GET"])
@token_required
def get_course_assignments(current_user, course_id):

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                id,
                course_id,
                title,
                description,
                due_date,
                created_at
            FROM assignments
            WHERE course_id = %s
            ORDER BY due_date ASC
        """, (course_id,))

        rows = cur.fetchall()

        assignments = []

        for row in rows:

            assignments.append({
                "id": row[0],
                "course_id": row[1],
                "title": row[2],
                "description": row[3],
                "due_date": str(row[4]),
                "created_at": str(row[5])
            })

        return jsonify({
            "message": "Assignments fetched successfully",
            "count": len(assignments),
            "data": assignments
        }), 200

    except Exception as e:

        return jsonify({
            "message": "Failed to fetch assignments",
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()