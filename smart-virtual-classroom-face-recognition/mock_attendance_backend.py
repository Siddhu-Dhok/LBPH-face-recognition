# mock_attendance_backend.py
from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime, timezone

app = Flask(__name__)
CSV_FILE = "attendance.csv"

def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "timestamp_iso", "timestamp_unix"])

def already_marked_today(student_id, ts_iso):
    # ts_iso is ISO string - check same calendar date in UTC
    try:
        ts = datetime.fromisoformat(ts_iso)
    except Exception:
        # fallback: treat as not marked
        return False
    date = ts.date()
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["student_id"] == student_id:
                try:
                    existing_ts = datetime.fromisoformat(row["timestamp_iso"])
                    if existing_ts.date() == date:
                        return True
                except Exception:
                    continue
    return False

@app.route("/api/attendance/mark", methods=["POST"])
def mark_attendance():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    student_id = data.get("student_id")
    timestamp = data.get("timestamp")  # expect ISO format
    if not student_id:
        return jsonify({"error": "missing student_id"}), 400

    # if timestamp missing, set to now UTC
    if not timestamp:
        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

    ensure_csv_exists()

    # prevent duplicate marking for same calendar date
    if already_marked_today(student_id, timestamp):
        return jsonify({"status": "already_marked"}), 200

    unix_ts = int(datetime.fromisoformat(timestamp).timestamp()) if "T" in timestamp else int(datetime.utcnow().timestamp())

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([student_id, timestamp, unix_ts])

    print(f"Marked attendance: {student_id} at {timestamp}")
    return jsonify({"status": "marked"}), 200

@app.route("/api/attendance/list", methods=["GET"])
def list_attendance():
    ensure_csv_exists()
    rows = []
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return jsonify(rows), 200

if __name__ == "__main__":
    # run on port 8000 to match recognition_service.py config
    app.run(host="127.0.0.1", port=8000, debug=False)