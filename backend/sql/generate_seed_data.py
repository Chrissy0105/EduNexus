import os
import random
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
from werkzeug.security import generate_password_hash

load_dotenv()

# Database connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

# Project requirements
NUM_STUDENTS = 100000
NUM_LECTURERS = 50
NUM_COURSES = 200
ASSIGNMENTS_PER_COURSE = 5

DEFAULT_PASSWORD = generate_password_hash("Jamaicakl#1")

# Clear old generated data
print("Clearing old data...")

cur.execute("""
    TRUNCATE TABLE
        grades,
        submissions,
        assignments,
        calendar_events,
        replies,
        threads,
        forums,
        course_enrollments,
        courses,
        users
    RESTART IDENTITY CASCADE;
""")

conn.commit()

# Create admin user
print("Creating admin user...")

cur.execute("""
    INSERT INTO users (full_name, email, password_hash, role)
    VALUES (%s, %s, %s, %s)
""", (
    "EduNexus Admin",
    "admin@edunexus.com",
    DEFAULT_PASSWORD,
    "admin"
))

conn.commit()

# Create lecturers
print("Creating lecturers...")

lecturers = []

for i in range(1, NUM_LECTURERS + 1):
    lecturers.append((
        f"Lecturer {i}",
        f"lecturer{i}@edunexus.com",
        DEFAULT_PASSWORD,
        "lecturer"
    ))

execute_values(cur, """
    INSERT INTO users (full_name, email, password_hash, role)
    VALUES %s
""", lecturers)

conn.commit()

# Create students
print("Creating students...")

students = []

for i in range(1, NUM_STUDENTS + 1):
    students.append((
        f"Student {i}",
        f"student{i}@edunexus.com",
        DEFAULT_PASSWORD,
        "student"
    ))

execute_values(cur, """
    INSERT INTO users (full_name, email, password_hash, role)
    VALUES %s
""", students, page_size=5000)

conn.commit()

# Get lecturer IDs
cur.execute("""
    SELECT user_id
    FROM users
    WHERE role = 'lecturer'
    ORDER BY user_id
""")

lecturer_ids = [row[0] for row in cur.fetchall()]

# Get student IDs
cur.execute("""
    SELECT user_id
    FROM users
    WHERE role = 'student'
    ORDER BY user_id
""")

student_ids = [row[0] for row in cur.fetchall()]

# Create courses
print("Creating courses...")

courses = []

for i in range(1, NUM_COURSES + 1):
    lecturer_id = lecturer_ids[(i - 1) % NUM_LECTURERS]

    courses.append((
        f"COMP{i:04d}",
        f"EduNexus Course {i}",
        f"Generated course number {i}",
        lecturer_id
    ))

execute_values(cur, """
    INSERT INTO courses (
        course_code,
        course_name,
        description,
        lecturer_id
    )
    VALUES %s
""", courses)

conn.commit()

# Get course IDs
cur.execute("""
    SELECT course_id
    FROM courses
    ORDER BY course_id
""")

course_ids = [row[0] for row in cur.fetchall()]

# Enroll students
print("Enrolling students in courses...")

enrollments = []

for student_id in student_ids:
    number_of_courses = random.randint(3, 6)
    selected_courses = random.sample(course_ids, number_of_courses)

    for course_id in selected_courses:
        enrollments.append((student_id, course_id))

execute_values(cur, """
    INSERT INTO course_enrollments (
        student_id,
        course_id
    )
    VALUES %s
    ON CONFLICT (student_id, course_id) DO NOTHING
""", enrollments, page_size=10000)

conn.commit()

# Generate forums
print("Generating forums...")

forums = []

for course_id in course_ids:
    forums.append((course_id, "General Discussion"))

execute_values(cur, """
    INSERT INTO forums (
        course_id,
        title
    )
    VALUES %s
""", forums)

conn.commit()

# Get forum IDs
cur.execute("""
    SELECT forum_id, course_id
    FROM forums
""")

forum_rows = cur.fetchall()

# Generate threads
print("Generating threads...")

threads = []

for forum_id, course_id in forum_rows:

    cur.execute("""
        SELECT student_id
        FROM course_enrollments
        WHERE course_id = %s
        LIMIT 5
    """, (course_id,))

    course_students = cur.fetchall()

    for student in course_students:
        student_id = student[0]

        threads.append((
            forum_id,
            student_id,
            "Welcome Thread",
            "This is an auto-generated discussion thread."
        ))

execute_values(cur, """
    INSERT INTO threads (
        forum_id,
        user_id,
        title,
        content
    )
    VALUES %s
""", threads, page_size=5000)

conn.commit()

# Get thread IDs
cur.execute("""
    SELECT thread_id, user_id
    FROM threads
""")

thread_rows = cur.fetchall()

# Generate replies
print("Generating replies...")

replies = []

for thread_id, user_id in thread_rows:
    replies.append((
        thread_id,
        user_id,
        "This is an auto-generated reply."
    ))

execute_values(cur, """
    INSERT INTO replies (
        thread_id,
        user_id,
        content
    )
    VALUES %s
""", replies, page_size=5000)

conn.commit()

# Generate assignments
print("Generating assignments...")

assignments = []

for course_id in course_ids:

    for i in range(1, ASSIGNMENTS_PER_COURSE + 1):

        assignments.append((
            course_id,
            f"Assignment {i}",
            f"Generated assignment {i} for course {course_id}",
            f"2026-12-{random.randint(1, 28)} 23:59:00"
        ))

execute_values(cur, """
    INSERT INTO assignments (
        course_id,
        title,
        description,
        due_date
    )
    VALUES %s
""", assignments, page_size=5000)

conn.commit()

# Get assignment IDs
cur.execute("""
    SELECT assignment_id, course_id
    FROM assignments
""")

assignment_rows = cur.fetchall()

# Generate submissions
print("Generating submissions...")

submissions = []

for assignment_id, course_id in assignment_rows:

    cur.execute("""
        SELECT student_id
        FROM course_enrollments
        WHERE course_id = %s
    """, (course_id,))

    enrolled_students = cur.fetchall()

    for student in enrolled_students:

        student_id = student[0]

        if random.random() < 0.85:
            submissions.append((
                assignment_id,
                student_id,
                f"Submission for assignment {assignment_id}"
            ))

execute_values(cur, """
    INSERT INTO submissions (
        assignment_id,
        student_id,
        submission_text
    )
    VALUES %s
""", submissions, page_size=10000)

conn.commit()

# Get submission IDs
cur.execute("""
    SELECT submission_id
    FROM submissions
""")

submission_rows = cur.fetchall()

# Generate grades
print("Generating grades...")

grades = []

for submission in submission_rows:

    submission_id = submission[0]
    lecturer_id = random.choice(lecturer_ids)

    grades.append((
        submission_id,
        lecturer_id,
        random.randint(50, 100),
        "Auto-generated feedback"
    ))

execute_values(cur, """
    INSERT INTO grades (
        submission_id,
        lecturer_id,
        grade,
        feedback
    )
    VALUES %s
""", grades, page_size=10000)

conn.commit()

# Generate calendar events
print("Generating calendar events...")

calendar_events = []

for course_id in course_ids:

    lecturer_id = lecturer_ids[(course_id - 1) % NUM_LECTURERS]

    calendar_events.append((
        course_id,
        lecturer_id,
        "Assignment Deadline",
        "Auto-generated course calendar event.",
        f"2026-12-{random.randint(1, 28)} 23:59:00"
    ))

execute_values(cur, """
    INSERT INTO calendar_events (
        course_id,
        creator_id,
        title,
        description,
        event_date
    )
    VALUES %s
""", calendar_events, page_size=5000)

conn.commit()

# Verify requirements
print("Verifying requirements...")

cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
student_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM users WHERE role = 'lecturer'")
lecturer_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM courses")
course_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM assignments")
assignment_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM submissions")
submission_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM grades")
grade_count = cur.fetchone()[0]

cur.execute("""
    SELECT MAX(course_count)
    FROM (
        SELECT COUNT(*) AS course_count
        FROM course_enrollments
        GROUP BY student_id
    ) AS student_courses
""")
max_courses_per_student = cur.fetchone()[0]

cur.execute("""
    SELECT MIN(course_count)
    FROM (
        SELECT COUNT(*) AS course_count
        FROM course_enrollments
        GROUP BY student_id
    ) AS student_courses
""")
min_courses_per_student = cur.fetchone()[0]

cur.execute("""
    SELECT MIN(member_count)
    FROM (
        SELECT COUNT(*) AS member_count
        FROM course_enrollments
        GROUP BY course_id
    ) AS course_members
""")
min_members_per_course = cur.fetchone()[0]

cur.execute("""
    SELECT MAX(course_count)
    FROM (
        SELECT COUNT(*) AS course_count
        FROM courses
        GROUP BY lecturer_id
    ) AS lecturer_courses
""")
max_courses_per_lecturer = cur.fetchone()[0]

cur.execute("""
    SELECT MIN(course_count)
    FROM (
        SELECT COUNT(*) AS course_count
        FROM courses
        GROUP BY lecturer_id
    ) AS lecturer_courses
""")
min_courses_per_lecturer = cur.fetchone()[0]

print("Seed data generated successfully.")
print(f"Students: {student_count}")
print(f"Lecturers: {lecturer_count}")
print(f"Courses: {course_count}")
print(f"Assignments: {assignment_count}")
print(f"Submissions: {submission_count}")
print(f"Grades: {grade_count}")
print(f"Student course range: {min_courses_per_student} - {max_courses_per_student}")
print(f"Minimum members per course: {min_members_per_course}")
print(f"Lecturer teaching range: {min_courses_per_lecturer} - {max_courses_per_lecturer}")

cur.close()
conn.close()