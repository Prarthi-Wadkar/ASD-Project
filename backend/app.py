
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import init_db, get_db

app = Flask(__name__)
CORS(app)

init_db()


@app.route("/")
def home():
    return jsonify({"message": "Lost & Found Backend is running"})


@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json(silent=True) or {}

    required = ["title", "description", "location", "date"]
    if not all(field in data for field in required):
        return jsonify({"message": "Missing required item fields"}), 400

    category = data.get("category", "lost")

    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO items (title, description, category, location, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        category,
        data["location"],
        data["date"]
    ))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Item created successfully",
        "id": item_id
    }), 201


@app.route("/api/items", methods=["GET"])
def get_items():
    category = request.args.get("category")
    conn = get_db()

    if category:
        items = conn.execute(
            "SELECT * FROM items WHERE category = ?", (category,)
        ).fetchall()
    else:
        items = conn.execute("SELECT * FROM items").fetchall()

    conn.close()
    return jsonify([dict(item) for item in items])


@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    conn = get_db()
    item = conn.execute(
        "SELECT * FROM items WHERE id = ?", (item_id,)
    ).fetchone()
    conn.close()

    if item is None:
        return jsonify({"message": "Item not found"}), 404

    return jsonify(dict(item))


@app.route("/api/claims", methods=["POST"])
def create_claim():
    data = request.get_json(silent=True) or {}

    if "item_id" not in data or not data.get("claimant_name"):
        return jsonify({"message": "item_id and claimant_name are required"}), 400

    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO claims (item_id, claimant_name)
        VALUES (?, ?)
    """, (data["item_id"], data["claimant_name"]))
    conn.commit()
    claim_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Claim created successfully",
        "id": claim_id
    }), 201


@app.route("/api/items/<int:item_id>/status", methods=["PUT"])
def update_status(item_id):
    data = request.get_json(silent=True) or {}

    if not data.get("status"):
        return jsonify({"message": "status is required"}), 400

    conn = get_db()
    cursor = conn.execute(
        "UPDATE items SET status = ? WHERE id = ?",
        (data["status"], item_id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Item not found"}), 404

    conn.close()
    return jsonify({"message": "Item status updated successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
