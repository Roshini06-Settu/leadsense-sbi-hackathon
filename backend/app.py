from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import time
from scoring import calculate_score

app = Flask(__name__)
CORS(app)

DB_FILE = "leads.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT,
            pages_visited INTEGER,
            time_on_site_seconds INTEGER,
            used_calculator INTEGER,
            started_application INTEGER,
            completed_application INTEGER,
            revisits INTEGER,
            score INTEGER,
            label TEXT,
            reason TEXT,
            updated_at INTEGER
        )
    """)
    conn.commit()
    conn.close()


@app.route("/track", methods=["POST"])
def track_event():
    """Receives visitor activity data and returns/stores the lead score."""
    data = request.get_json()
    visitor_id = data.get("visitor_id", "anonymous")

    events = {
        "pages_visited": data.get("pages_visited", 0),
        "time_on_site_seconds": data.get("time_on_site_seconds", 0),
        "used_calculator": data.get("used_calculator", False),
        "started_application": data.get("started_application", False),
        "completed_application": data.get("completed_application", False),
        "revisits": data.get("revisits", 0),
    }

    result = calculate_score(events)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO leads (visitor_id, pages_visited, time_on_site_seconds,
                            used_calculator, started_application, completed_application,
                            revisits, score, label, reason, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        visitor_id,
        events["pages_visited"],
        events["time_on_site_seconds"],
        int(events["used_calculator"]),
        int(events["started_application"]),
        int(events["completed_application"]),
        events["revisits"],
        result["score"],
        result["label"],
        result["reason"],
        int(time.time())
    ))
    conn.commit()
    conn.close()

    return jsonify({"visitor_id": visitor_id, **result})


@app.route("/leads", methods=["GET"])
def get_leads():
    """Returns all leads ranked by score, highest first."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM leads ORDER BY score DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(rows)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "LeadSense API is running."})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
