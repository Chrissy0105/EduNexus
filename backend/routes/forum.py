from flask import Blueprint, request, jsonify
from db import get_db_connection

forum_bp = Blueprint("forum", __name__)

# -----------------------------
# CREATE THREAD
# POST /api/v1/threads
# -----------------------------
@forum_bp.route("/threads", methods=["POST"])
def create_thread():
    data = request.json

    forum_id = data.get("forum_id")
    title = data.get("title")
    content = data.get("content")

    if not forum_id or not title or not content:
        return jsonify({"message": "Missing fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO threads (forum_id, title, content)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (forum_id, title, content))

    thread_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Thread created",
        "thread_id": thread_id,
        "data": data
    }), 201


# -----------------------------
# GET THREAD REPLIES
# GET /api/v1/threads/<id>/replies
# -----------------------------
@forum_bp.route("/threads/<int:thread_id>/replies", methods=["GET"])
def get_replies(thread_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, thread_id, content
        FROM replies
        WHERE thread_id = %s
        ORDER BY id ASC
    """, (thread_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    replies = []
    for r in rows:
        replies.append({
            "id": r[0],
            "thread_id": r[1],
            "content": r[2]
        })

    return jsonify({
        "message": "Replies fetched successfully",
        "data": replies
    }), 200


# -----------------------------
# CREATE REPLY
# POST /api/v1/replies
# -----------------------------
@forum_bp.route("/replies", methods=["POST"])
def create_reply():
    data = request.json

    thread_id = data.get("thread_id")
    content = data.get("content")

    if not thread_id or not content:
        return jsonify({"message": "Missing fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO replies (thread_id, content)
        VALUES (%s, %s)
        RETURNING id
    """, (thread_id, content))

    reply_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Reply created",
        "reply_id": reply_id
    }), 201