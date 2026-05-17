from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import jwt
import datetime
import os

auth_bp = Blueprint("auth_bp", __name__)
SECRET = os.getenv("JWT_SECRET", "edunexus-secret")


# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "student")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"message": "User already exists"}), 409

        hashed = generate_password_hash(password)

        cur.execute("""
            INSERT INTO users (full_name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, hashed, role))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User registered"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json

        email = data.get("email")
        password = data.get("password")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, full_name, email, password_hash, role
            FROM users WHERE email = %s
        """, (email,))

        user = cur.fetchone()

        if not user:
            return jsonify({"message": "User not found"}), 404

        user_id, full_name, email, password_hash, role = user

        if not check_password_hash(password_hash, password):
            return jsonify({"message": "Invalid password"}), 401

        token = jwt.encode({
            "user_id": user_id,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET, algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user_id,
                "full_name": full_name,
                "email": email,
                "role": role
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500