from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import jwt
import datetime

routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/")
def home():

    return jsonify({
        "message": "Welcome to EduNexus API"
    })


@routes_bp.route("/test-db")
def test_db():

    conn = get_db_connection()

    if conn:
        conn.close()

        return jsonify({
            "success": True,
            "message": "Database connected!"
        })

    return jsonify({
        "success": False,
        "message": "Database connection failed"
    })


@routes_bp.route("/api/v1/auth/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not full_name or not email or not password or not role:

        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if email already exists
        cur.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:

            cur.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "Email already exists"
            }), 409

        # Hash password
        password_hash = generate_password_hash(password)

        # Insert user
        cur.execute("""
            INSERT INTO users (
                full_name,
                email,
                password_hash,
                role
            )
            VALUES (%s, %s, %s, %s)
        """, (
            full_name,
            email,
            password_hash,
            role
        ))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "User registered successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@routes_bp.route("/api/v1/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT user_id,
                   full_name,
                   email,
                   password_hash,
                   role
            FROM users
            WHERE email = %s
        """, (email,))

        user = cur.fetchone()

        cur.close()
        conn.close()

        if not user:

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        user_id, full_name, email, password_hash, role = user

        if not check_password_hash(password_hash, password):

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        # Generate JWT token
        token = jwt.encode({
            "user_id": user_id,
            "email": email,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        "edunexus_secret_key",
        algorithm="HS256")

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "user_id": user_id,
                "full_name": full_name,
                "email": email,
                "role": role
            }
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
@routes_bp.route("/api/v1/courses", methods=["POST"])
def create_course():

    data = request.get_json()

    course_code = data.get("course_code")
    course_name = data.get("course_name")
    description = data.get("description")
    lecturer_id = data.get("lecturer_id")

    if not course_code or not course_name:

        return jsonify({
            "success": False,
            "message": "Course code and course name are required"
        }), 400

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if course already exists
        cur.execute(
            "SELECT course_id FROM courses WHERE course_code = %s",
            (course_code,)
        )

        existing_course = cur.fetchone()

        if existing_course:

            cur.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "Course already exists"
            }), 409

        # Insert course
        cur.execute("""
            INSERT INTO courses (
                course_code,
                course_name,
                description,
                lecturer_id
            )
            VALUES (%s, %s, %s, %s)
        """, (
            course_code,
            course_name,
            description,
            lecturer_id
        ))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Course created successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

@routes_bp.route("/api/v1/courses", methods=["GET"])
def get_courses():

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                c.course_id,
                c.course_code,
                c.course_name,
                c.description,
                c.created_at,
                u.full_name AS lecturer_name
            FROM courses c
            LEFT JOIN users u
                ON c.lecturer_id = u.user_id
            ORDER BY c.course_id ASC
        """)

        courses = cur.fetchall()

        cur.close()
        conn.close()

        course_list = []

        for course in courses:

            course_list.append({
                "course_id": course[0],
                "course_code": course[1],
                "course_name": course[2],
                "description": course[3],
                "created_at": course[4],
                "lecturer_name": course[5]
            })

        return jsonify({
            "success": True,
            "courses": course_list
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/courses/enroll", methods=["POST"])
def enroll_course():

    data = request.get_json()

    student_id = data.get("student_id")
    course_id = data.get("course_id")

    if not student_id or not course_id:

        return jsonify({
            "success": False,
            "message": "Student ID and Course ID are required"
        }), 400

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if already enrolled
        cur.execute("""
            SELECT enrollment_id
            FROM course_enrollments
            WHERE student_id = %s
            AND course_id = %s
        """, (student_id, course_id))

        existing_enrollment = cur.fetchone()

        if existing_enrollment:

            cur.close()
            conn.close()

            return jsonify({
                "success": False,
                "message": "Student already enrolled"
            }), 409

        # Insert enrollment
        cur.execute("""
            INSERT INTO course_enrollments (
                student_id,
                course_id
            )
            VALUES (%s, %s)
        """, (student_id, course_id))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Student enrolled successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/courses/<int:course_id>/students", methods=["GET"])
def get_course_students(course_id):

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                u.user_id,
                u.full_name,
                u.email,
                u.role,
                ce.enrolled_at
            FROM course_enrollments ce
            JOIN users u
                ON ce.student_id = u.user_id
            WHERE ce.course_id = %s
            ORDER BY u.full_name ASC
        """, (course_id,))

        students = cur.fetchall()

        cur.close()
        conn.close()

        student_list = []

        for student in students:

            student_list.append({
                "user_id": student[0],
                "full_name": student[1],
                "email": student[2],
                "role": student[3],
                "enrolled_at": student[4]
            })

        return jsonify({
            "success": True,
            "students": student_list
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/forums", methods=["POST"])
def create_forum():

    data = request.get_json()

    course_id = data.get("course_id")
    title = data.get("title")

    if not course_id or not title:
        return jsonify({
            "success": False,
            "message": "Course ID and forum title are required"
        }), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO forums (course_id, title)
            VALUES (%s, %s)
        """, (course_id, title))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Forum created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/threads", methods=["POST"])
def create_thread():

    data = request.get_json()

    forum_id = data.get("forum_id")
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")

    if not forum_id or not user_id or not title or not content:

        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO threads (
                forum_id,
                user_id,
                title,
                content
            )
            VALUES (%s, %s, %s, %s)
        """, (
            forum_id,
            user_id,
            title,
            content
        ))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Thread created successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/replies", methods=["POST"])
def create_reply():

    data = request.get_json()

    thread_id = data.get("thread_id")
    user_id = data.get("user_id")
    content = data.get("content")

    if not thread_id or not user_id or not content:
        return jsonify({
            "success": False,
            "message": "Thread ID, User ID and content are required"
        }), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO replies (thread_id, user_id, content)
            VALUES (%s, %s, %s)
        """, (thread_id, user_id, content))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Reply created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/threads/<int:thread_id>/replies", methods=["GET"])
def get_thread_replies(thread_id):

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                r.reply_id,
                r.content,
                r.created_at,
                u.user_id,
                u.full_name,
                u.role
            FROM replies r
            JOIN users u
                ON r.user_id = u.user_id
            WHERE r.thread_id = %s
            ORDER BY r.created_at ASC
        """, (thread_id,))

        replies = cur.fetchall()

        cur.close()
        conn.close()

        reply_list = []

        for reply in replies:

            reply_list.append({
                "reply_id": reply[0],
                "content": reply[1],
                "created_at": reply[2],
                "user": {
                    "user_id": reply[3],
                    "full_name": reply[4],
                    "role": reply[5]
                }
            })

        return jsonify({
            "success": True,
            "replies": reply_list
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/assignments", methods=["POST"])
def create_assignment():

    data = request.get_json()

    course_id = data.get("course_id")
    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")

    if not course_id or not title or not due_date:
        return jsonify({
            "success": False,
            "message": "Course ID, title and due date are required"
        }), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO assignments (course_id, title, description, due_date)
            VALUES (%s, %s, %s, %s)
        """, (course_id, title, description, due_date))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Assignment created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/submissions", methods=["POST"])
def create_submission():

    data = request.get_json()

    assignment_id = data.get("assignment_id")
    student_id = data.get("student_id")
    submission_text = data.get("submission_text")

    if not assignment_id or not student_id or not submission_text:
        return jsonify({
            "success": False,
            "message": "Assignment ID, Student ID and submission text are required"
        }), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO submissions (
                assignment_id,
                student_id,
                submission_text
            )
            VALUES (%s, %s, %s)
        """, (
            assignment_id,
            student_id,
            submission_text
        ))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Submission uploaded successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
@routes_bp.route("/api/v1/grades", methods=["POST"])
def grade_submission():

    data = request.get_json()

    submission_id = data.get("submission_id")
    lecturer_id = data.get("lecturer_id")
    grade = data.get("grade")
    feedback = data.get("feedback")

    if submission_id is None or lecturer_id is None or grade is None:
        return jsonify({
            "success": False,
            "message": "Submission ID, lecturer ID and grade are required"
        }), 400

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO grades (
                submission_id,
                lecturer_id,
                grade,
                feedback
            )
            VALUES (%s, %s, %s, %s)
        """, (
            submission_id,
            lecturer_id,
            grade,
            feedback
        ))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Submission graded successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/courses/<int:course_id>/assignments", methods=["GET"])
def get_course_assignments(course_id):

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                assignment_id,
                course_id,
                title,
                description,
                due_date,
                created_at
            FROM assignments
            WHERE course_id = %s
            ORDER BY due_date ASC
        """, (course_id,))

        assignments = cur.fetchall()

        cur.close()
        conn.close()

        assignment_list = []

        for assignment in assignments:
            assignment_list.append({
                "assignment_id": assignment[0],
                "course_id": assignment[1],
                "title": assignment[2],
                "description": assignment[3],
                "due_date": assignment[4],
                "created_at": assignment[5]
            })

        return jsonify({
            "success": True,
            "assignments": assignment_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/calendar-events", methods=["POST"])
def create_calendar_event():

    data = request.get_json()

    course_id = data.get("course_id")
    creator_id = data.get("creator_id")
    title = data.get("title")
    description = data.get("description")
    event_date = data.get("event_date")

    if not course_id or not creator_id or not title or not event_date:
        return jsonify({
            "success": False,
            "message": "Course ID, creator ID, title and event date are required"
        }), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO calendar_events (
                course_id,
                creator_id,
                title,
                description,
                event_date
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            course_id,
            creator_id,
            title,
            description,
            event_date
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Calendar event created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@routes_bp.route("/api/v1/courses/<int:course_id>/calendar-events", methods=["GET"])
def get_course_calendar_events(course_id):

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                ce.event_id,
                ce.title,
                ce.description,
                ce.event_date,
                ce.created_at,
                u.full_name
            FROM calendar_events ce
            JOIN users u
                ON ce.creator_id = u.user_id
            WHERE ce.course_id = %s
            ORDER BY ce.event_date ASC
        """, (course_id,))

        events = cur.fetchall()

        cur.close()
        conn.close()

        event_list = []

        for event in events:
            event_list.append({
                "event_id": event[0],
                "title": event[1],
                "description": event[2],
                "event_date": event[3],
                "created_at": event[4],
                "created_by": event[5]
            })

        return jsonify({
            "success": True,
            "events": event_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500