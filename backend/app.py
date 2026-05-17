from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "message": "Welcome to EduNexus API"
    }

CORS(app)

from routes.auth import auth_bp
from routes.courses import courses_bp
from routes.forum import forum_bp
from routes.threads import threads_bp
from routes.assignments import assignments_bp
from routes.submissions import submissions_bp
from routes.grades import grades_bp
from routes.calendar_events import calendar_bp

app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
app.register_blueprint(courses_bp, url_prefix="/api/v1/courses")
app.register_blueprint(forum_bp, url_prefix="/api/v1")
app.register_blueprint(threads_bp, url_prefix="/api/v1/threads")
app.register_blueprint(assignments_bp, url_prefix="/api/v1")
app.register_blueprint(submissions_bp, url_prefix="/api/v1")
app.register_blueprint(grades_bp, url_prefix="/api/v1")
app.register_blueprint(calendar_bp, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(debug=True)
