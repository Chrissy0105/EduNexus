# EduNexus Backend API

## Overview

EduNexus is a university course management backend system built using Flask, PostgreSQL, and JWT authentication. The system supports course management, enrollments, assignments, forums, grading, and calendar event management.

The backend was designed to support large-scale academic datasets and includes automated seed data generation for over 100,000 students.

---

# Features

## Authentication & Authorization

* User registration
* User login
* JWT authentication
* Role-based authorization
* Protected API routes

## User Roles

* Admin
* Lecturer
* Student

## Course Management

* Create courses
* View courses
* Enroll students into courses
* View enrolled students

## Forum System

* Create forums
* Create discussion threads
* Reply to threads
* View thread replies

## Assignment System

* Create assignments
* Submit assignments
* Grade submissions
* View course assignments

## Calendar Events

* Create course calendar events
* View course calendar events

## Database Features

* PostgreSQL relational database
* SQL views for analytical reporting
* Large-scale seed data generation
* Supports over 100,000 students

---

# Technologies Used

| Technology    | Purpose                     |
| ------------- | --------------------------- |
| Flask         | Backend framework           |
| PostgreSQL    | Relational database         |
| Psycopg2      | PostgreSQL database adapter |
| JWT           | Authentication              |
| Werkzeug      | Password hashing            |
| Python Dotenv | Environment variables       |
| Postman       | API testing                 |

---

# Project Structure

```txt
backend/
│
├── app.py
├── routes.py
├── db.py
├── config.py
├── requirements.txt
├── .env
│
├── sql/
│   ├── schema.sql
│   ├── views.sql
│   └── generate_seed_data.py
│
├── EduNexus.postman_collection.json
│
└── README.md
```

---

# Environment Variables

Create a `.env` file in the backend directory.

Example:

```env
DB_HOST=localhost
DB_NAME=edunexus
DB_USER=course_user
DB_PASSWORD=your_password
DB_PORT=5432
SECRET_KEY=edunexus_secret_key
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/EduNexus.git
cd EduNexus/backend
```

---

# Create Virtual Environment

```bash
python3 -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Database Setup

## Create Database

```sql
CREATE DATABASE edunexus;
```

## Create User

```sql
CREATE USER course_user WITH PASSWORD 'your_password';
```

## Grant Permissions

```sql
GRANT ALL PRIVILEGES ON DATABASE edunexus TO course_user;
GRANT ALL ON SCHEMA public TO course_user;
```

---

# Create Database Tables

Run:

```bash
psql -h localhost -U course_user -d edunexus -f sql/schema.sql
```

---

# Create SQL Views

Run:

```bash
psql -h localhost -U course_user -d edunexus -f sql/views.sql
```

---

# Generate Seed Data

The project includes a large-scale seed data generator.

Generated data includes:

* 100,000 students
* 50 lecturers
* 200 courses
* Forums
* Threads
* Replies
* Assignments
* Submissions
* Grades
* Calendar events

Run:

```bash
python sql/generate_seed_data.py
```

---

# Run Flask Application

Start the backend server:

```bash
python app.py
```

Server URL:

```txt
http://127.0.0.1:5000
```

---

# JWT Authentication

Protected routes require a JWT token.

Login route:

```txt
POST /api/v1/auth/login
```

Use the returned token in Postman headers:

```txt
Authorization: Bearer your_token_here
```

---

# API Endpoints

## Authentication

| Method | Endpoint              | Description   |
| ------ | --------------------- | ------------- |
| POST   | /api/v1/auth/register | Register user |
| POST   | /api/v1/auth/login    | Login user    |

---

## Courses

| Method | Endpoint                      | Description           |
| ------ | ----------------------------- | --------------------- |
| POST   | /api/v1/courses               | Create course         |
| GET    | /api/v1/courses               | Get courses           |
| POST   | /api/v1/courses/enroll        | Enroll course         |
| GET    | /api/v1/courses/<id>/students | Get enrolled students |

---

## Forums

| Method | Endpoint                     | Description        |
| ------ | ---------------------------- | ------------------ |
| POST   | /api/v1/forums               | Create forum       |
| POST   | /api/v1/threads              | Create thread      |
| POST   | /api/v1/replies              | Create reply       |
| GET    | /api/v1/threads/<id>/replies | Get thread replies |

---

## Assignments

| Method | Endpoint                         | Description       |
| ------ | -------------------------------- | ----------------- |
| POST   | /api/v1/assignments              | Create assignment |
| POST   | /api/v1/submissions              | Submit assignment |
| POST   | /api/v1/grades                   | Grade submission  |
| GET    | /api/v1/courses/<id>/assignments | Get assignments   |

---

## Calendar Events

| Method | Endpoint                             | Description  |
| ------ | ------------------------------------ | ------------ |
| POST   | /api/v1/calendar-events              | Create event |
| GET    | /api/v1/courses/<id>/calendar-events | Get events   |

---

# SQL Views

The project includes analytical SQL views.

## Available Views

* courses_with_50_or_more_students
* students_with_5_or_more_courses
* lecturers_teaching_3_or_more_courses
* top_10_most_enrolled_courses
* top_10_students_highest_averages

---

# Postman Collection

Import the Postman collection file:

```txt
EduNexus.postman_collection.json
```

In Postman:

```txt
Import → File → Select JSON File
```

---

# Testing

The backend APIs were tested using Postman.

Testing included:

* Authentication
* Authorization
* Role protection
* CRUD operations
* Database integration
* Large-scale seed data generation
* SQL analytical views

---

# Sample Login Credentials

## Admin

```txt
Email: admin@edunexus.com
Password: Jamaicakl#1
```

## Lecturer

```txt
Email: lecturer1@edunexus.com
Password: Jamaicakl#1
```

## Student

```txt
Email: student1@edunexus.com
Password: Jamaicakl#1
```

---

# Future Improvements

* File uploads
* Email notifications
* Real-time chat
* Pagination
* Docker deployment
* Unit testing
* API rate limiting
* Redis caching
* Frontend integration

---

# Author

EduNexus Backend System

Built using Flask and PostgreSQL.
