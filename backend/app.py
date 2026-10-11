
from datetime import date
import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from database import get_connection, init_db

# Make the existing matching engine available without moving its files.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MATCHING_DIR = PROJECT_ROOT / "matching"
sys.path.insert(0, str(MATCHING_DIR))

from matcher import match_items


app = Flask(__name__)
CORS(app)


def serialize_item(item):
    item = dict(item)
    item["date"] = item.pop("item_date").isoformat()
    item["created_at"] = item["created_at"].isoformat()
    return item


def create_item(item_type):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON request body is required."}), 400

    title = data.get("title")
    description = data.get("description")
    location = data.get("location")
    item_date = data.get("date")
    category = data.get("category", "other")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (title, description, location, item_date, category)
    ):
        return jsonify({
            "error": "Title, description, location, date and category are required."
        }), 400

    if len(title) > 200 or len(location) > 200 or len(category) > 100:
        return jsonify({"error": "One or more fields exceed the allowed length."}), 400

    try:
        parsed_date = date.fromisoformat(item_date)
    except ValueError:
        return jsonify({"error": "Date must use YYYY-MM-DD format."}), 400

    with get_connection() as conn:
        item = conn.execute("""
            INSERT INTO items
                (item_type, title, description, category, location, item_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            item_type,
            title.strip(),
            description.strip(),
            category.strip(),
            location.strip(),
            parsed_date
        )).fetchone()

    return jsonify(serialize_item(item)), 201


@app.get("/api/health")
def health():
    with get_connection() as conn:
        conn.execute("SELECT 1")
    return jsonify({"status": "ok", "database": "connected"})


@app.post("/api/items/lost")
def report_lost():
    return create_item("lost")


@app.post("/api/items/found")
def report_found():
    return create_item("found")


@app.get("/api/items")
def get_items():
    item_type = request.args.get("type")

    if item_type not in (None, "lost", "found"):
        return jsonify({"error": "Type must be lost or found."}), 400

    with get_connection() as conn:
        if item_type:
            rows = conn.execute("""
                SELECT * FROM items
                WHERE item_type = %s
                ORDER BY created_at DESC
            """, (item_type,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM items
                ORDER BY created_at DESC
            """).fetchall()

    return jsonify([serialize_item(row) for row in rows])


@app.get("/api/matches/<int:lost_item_id>")
def get_matches(lost_item_id):
    with get_connection() as conn:
        lost_item = conn.execute("""
            SELECT * FROM items
            WHERE id = %s AND item_type = 'lost'
        """, (lost_item_id,)).fetchone()

        if lost_item is None:
            return jsonify({"error": "Lost item not found."}), 404

        found_items = conn.execute("""
            SELECT * FROM items
            WHERE item_type = 'found'
        """).fetchall()

    lost = {
        "id": lost_item["id"],
        "description": lost_item["description"],
        "category": lost_item["category"],
        "location": lost_item["location"],
        "date": lost_item["item_date"].isoformat()
    }

    results = []

    for item in found_items:
        found = {
            "id": item["id"],
            "description": item["description"],
            "category": item["category"],
            "location": item["location"],
            "date": item["item_date"].isoformat()
        }

        result = match_items(lost, found)
        result["found_item"] = serialize_item(item)
        results.append(result)

    results.sort(key=lambda result: result["score"], reverse=True)

    return jsonify({
        "lost_item": serialize_item(lost_item),
        "matches": results
    })


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
