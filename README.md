# EduNexus

EduNexus is a centralized course management system that connects students, lecturers, and administrators through a unified platform for learning, communication, and academic management.

---

## 🛠 Tech Stack

* **Frontend:** HTML, CSS, JavaScript (Vanilla)
* **Backend:** Flask (Python)
* **Database:** PostgreSQL
* **Environment:** WSL (Ubuntu)
* **API Testing:** Postman
* **Authentication:** JWT (JSON Web Tokens)
* **Database Access:** Raw SQL (psycopg2)

---

## 📦 Features

* User Registration & Login (Student, Lecturer, Admin)
* Course Creation & Enrollment
* Course Membership Management
* Forum Discussions (Threads & Replies)
* Course Content Management (Sections, Files, Links)
* Assignment Submission & Grading
* Calendar Events
* Reports & Analytics

---

## 🗂 Project Structure

```id="g1d9kp"
EduNexus/
│
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── config.py
│   ├── routes/
│   ├── sql/
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js
│   └── assets/
│
└── README.md
```

---

## ⚙️ Backend Setup

```bash id="6e3k8u"
git clone https://github.com/Chrissy0105/EduNexus.git
cd EduNexus/backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo service postgresql start

flask run
```

---

## 🌐 Frontend Setup

Since this is a static frontend, no build tools are required.

### Option 1: Open directly

```bash id="5v2h1u"
cd EduNexus/frontend
open index.html
```

### Option 2 (Recommended): Use Live Server (VS Code)

* Right-click `index.html`
* Click **"Open with Live Server"**

---

## 🔗 Backend–Frontend Connection

Frontend communicates with backend via:

```id="b6a0tg"
http://localhost:5000/api/v1
```

Example request:

```javascript id="4h3h7u"
fetch("http://localhost:5000/api/v1/courses")
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## ⚠️ Enable CORS (Required)

Install:

```bash id="3bp7c2"
pip install flask-cors
```

In `app.py`:

```python id="kz0q1p"
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

---

## 📡 API Contract (Frontend Integration)

### 🔐 Authentication

**POST** `/api/v1/auth/register`

```json id="j0o6qz"
{
  "name": "John Doe",
  "email": "john@gmail.com",
  "password": "123456",
  "role": "student"
}
```

---

**POST** `/api/v1/auth/login`

```json id="qnt8e4"
{
  "success": true,
  "token": "jwt_token_here"
}
```

---

### 📚 Courses

* **GET** `/api/v1/courses`
* **POST** `/api/v1/courses`
* **POST** `/api/v1/courses/:id/enroll`

---

### 💬 Forums & Threads

* **GET** `/api/v1/courses/:id/forums`
* **POST** `/api/v1/threads`
* **POST** `/api/v1/threads/:id/reply`

---

### 📁 Course Content

* **GET** `/api/v1/courses/:id/content`
* **POST** `/api/v1/content`

---

### 📝 Assignments

* **POST** `/api/v1/assignments/submit`
* **POST** `/api/v1/grades`

---

### 📊 Reports

* **GET** `/api/v1/reports/top-students`

---

## 🔄 Response Format

```json id="y8sj9g"
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

---

## 📌 Academic Requirements Covered

* REST API implementation
* Database design and normalization
* Large dataset handling (100,000+ students)
* Role-based system
* SQL Views for reporting
* Frontend + Backend integration (Bonus)

---

## 👨‍💻 Authors

* Christina Blye
* Christoff Cohen
* Joshua Henry
* Ruth-Ann Allen
* Jaden Jones

---

## 🚀 Future Improvements

* Better UI/UX design
* Deployment
* Dockerization
* Performance optimization
