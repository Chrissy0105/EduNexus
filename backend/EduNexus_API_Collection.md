# EduNexus Postman API Collection

## Base URL

```txt
http://127.0.0.1:5000
```

---

# Authentication

## Register User

### POST

```txt
/api/v1/auth/register
```

### Body

```json
{
  "full_name": "Test Student",
  "email": "teststudent@gmail.com",
  "password": "Jamaicakl#1",
  "role": "student"
}
```

---

## Login User

### POST

```txt
/api/v1/auth/login
```

### Body

```json
{
  "email": "teststudent@gmail.com",
  "password": "Jamaicakl#1"
}
```

---

# Courses

## Create Course

### POST

```txt
/api/v1/courses
```

### Headers

```txt
Authorization: Bearer your_admin_token
```

### Body

```json
{
  "course_code": "COMP3901",
  "course_name": "Final Year Project",
  "description": "Software engineering capstone project",
  "lecturer_id": 1
}
```

---

## Get Courses

### GET

```txt
/api/v1/courses
```

---

## Enroll Course

### POST

```txt
/api/v1/courses/enroll
```

### Headers

```txt
Authorization: Bearer your_student_token
```

### Body

```json
{
  "course_id": 1
}
```

---

## Get Course Students

### GET

```txt
/api/v1/courses/1/students
```

### Headers

```txt
Authorization: Bearer your_token
```

---

# Forums

## Create Forum

### POST

```txt
/api/v1/forums
```

### Headers

```txt
Authorization: Bearer your_token
```

### Body

```json
{
  "course_id": 1,
  "title": "General Discussion"
}
```

---

## Create Thread

### POST

```txt
/api/v1/threads
```

### Headers

```txt
Authorization: Bearer your_token
```

### Body

```json
{
  "forum_id": 1,
  "title": "Welcome Thread",
  "content": "Introduce yourself here."
}
```

---

## Create Reply

### POST

```txt
/api/v1/replies
```

### Headers

```txt
Authorization: Bearer your_token
```

### Body

```json
{
  "thread_id": 1,
  "content": "Hello everyone!"
}
```

---

## Get Thread Replies

### GET

```txt
/api/v1/threads/1/replies
```

### Headers

```txt
Authorization: Bearer your_token
```

---

# Assignments

## Create Assignment

### POST

```txt
/api/v1/assignments
```

### Headers

```txt
Authorization: Bearer your_lecturer_token
```

### Body

```json
{
  "course_id": 1,
  "title": "SQL Assignment",
  "description": "Practice joins and aggregation.",
  "due_date": "2026-05-20 23:59:00"
}
```

---

## Submit Assignment

### POST

```txt
/api/v1/submissions
```

### Headers

```txt
Authorization: Bearer your_student_token
```

### Body

```json
{
  "assignment_id": 1,
  "submission_text": "My completed assignment submission."
}
```

---

## Grade Submission

### POST

```txt
/api/v1/grades
```

### Headers

```txt
Authorization: Bearer your_lecturer_token
```

### Body

```json
{
  "submission_id": 1,
  "grade": 95,
  "feedback": "Excellent work."
}
```

---

## Get Course Assignments

### GET

```txt
/api/v1/courses/1/assignments
```

### Headers

```txt
Authorization: Bearer your_token
```

---

# Calendar Events

## Create Calendar Event

### POST

```txt
/api/v1/calendar-events
```

### Headers

```txt
Authorization: Bearer your_lecturer_token
```

### Body

```json
{
  "course_id": 1,
  "title": "Assignment Deadline",
  "description": "SQL Assignment Due",
  "event_date": "2026-05-20 23:59:00"
}
```

---

## Get Calendar Events

### GET

```txt
/api/v1/courses/1/calendar-events
```

### Headers

```txt
Authorization: Bearer your_token
```

---

# Notes

- All protected routes require a JWT token.
- Tokens are generated from the login route.
- Use the Authorization header for protected endpoints.
- Roles:
  - admin
  - lecturer
  - student

- Password hashing is handled using Werkzeug.
- JWT authentication is implemented using PyJWT.
- PostgreSQL is used as the database backend.
