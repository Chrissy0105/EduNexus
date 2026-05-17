from flask import Blueprint, request, jsonify
from db import get_db_connection
from middleware.auth_middleware import token_required

calendar_bp = Blueprint("calendar_bp", __name__)



# CREATE CALENDAR EVENT
@calendar_bp.route("/calendar-events", methods=["POST"])
@token_required
def create_calendar_event(current_user):

    data = request.json

    course_id = data.get("course_id")
    title = data.get("title")
    description = data.get("description")
    event_date = data.get("event_date")

    if not course_id or not title or not event_date:
        return jsonify({
            "message": "Missing required fields"
        }), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO calendar_events
            (course_id, title, description, event_date)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            course_id,
            title,
            description,
            event_date
        ))

        event_id = cur.fetchone()[0]

        conn.commit()

        return jsonify({
            "message": "Calendar event created successfully",
            "event_id": event_id,
            "data": {
                "course_id": course_id,
                "title": title,
                "description": description,
                "event_date": event_date
            }
        }), 201

    except Exception as e:

        conn.rollback()

        return jsonify({
            "message": "Failed to create calendar event",
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()



# GET COURSE CALENDAR EVENTS
@calendar_bp.route("/courses/<int:course_id>/calendar-events", methods=["GET"])
@token_required
def get_calendar_events(current_user, course_id):

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                id,
                course_id,
                title,
                description,
                event_date,
                created_at
            FROM calendar_events
            WHERE course_id = %s
            ORDER BY event_date ASC
        """, (course_id,))

        rows = cur.fetchall()

        events = []

        for row in rows:

            events.append({
                "id": row[0],
                "course_id": row[1],
                "title": row[2],
                "description": row[3],
                "event_date": str(row[4]),
                "created_at": str(row[5])
            })

        return jsonify({
            "message": "Calendar events fetched successfully",
            "count": len(events),
            "data": events
        }), 200

    except Exception as e:

        return jsonify({
            "message": "Failed to fetch calendar events",
            "error": str(e)
        }), 500

    finally:

        cur.close()
        conn.close()
