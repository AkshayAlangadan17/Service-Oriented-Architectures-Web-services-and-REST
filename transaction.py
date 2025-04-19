# -*- coding: utf-8 -*-
# Transaction Service
from flask import Flask, request, jsonify
import sqlite3, requests, logging
from datetime import datetime

app  = Flask(__name__)
logging.basicConfig(filename="transaction_service.log", level=logging.DEBUG)

AUTH_VERIFY_URL = "http://localhost:5000/auth/verify"

# -------------------  SQLite setup  -------------------
conn   = sqlite3.connect("transactions.db", check_same_thread=False)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS transactions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer   TEXT,
  timestamp  TEXT,
  status     TEXT,
  vendor_id  TEXT,
  amount     REAL
);
CREATE TABLE IF NOT EXISTS results(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  transaction_id INTEGER,
  timestamp      TEXT,
  is_fraudulent  BOOLEAN,
  confidence     REAL,
  FOREIGN KEY(transaction_id) REFERENCES transactions(id)
);
""")
conn.commit()

# -------------------  helper  -------------------
def verify_token(token:str):
    try:
        r = requests.get(AUTH_VERIFY_URL, headers={"Authorization": token})
        if r.status_code == 200:
            return r.json()    # {username, role}
    except Exception as e:
        logging.error("Error contacting auth service: %s", e)
    return None

# -------------------  routes  -------------------
@app.route("/transactions", methods=["POST"])
def add_transaction():
    token     = request.headers.get("Authorization", "")
    user_info = verify_token(token)
    logging.info("POST /transactions  user=%s  body=%s", user_info, request.json)

    if not user_info or user_info["role"] not in ("Administrator", "Agent"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    cursor.execute(
        "INSERT INTO transactions(customer, timestamp, status, vendor_id, amount) VALUES (?,?,?,?,?)",
        (data["customer"], datetime.now().isoformat(), data["status"], data["vendor_id"], data["amount"])
    )
    conn.commit()
    return jsonify({"success": "Transaction added"})

@app.route("/transactions/<int:tx_id>", methods=["PUT"])
def update_transaction(tx_id):
    token     = request.headers.get("Authorization", "")
    user_info = verify_token(token)
    logging.info("PUT /transactions/%s  user=%s  body=%s", tx_id, user_info, request.json)

    if not user_info or user_info["role"] not in ("Administrator", "Agent"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    cursor.execute("UPDATE transactions SET status=? WHERE id=?", (data["status"], tx_id))
    conn.commit()
    return jsonify({"success": "Transaction updated"})

@app.route("/results/<int:tx_id>", methods=["GET"])
def get_results(tx_id):
    token     = request.headers.get("Authorization", "")
    user_info = verify_token(token)
    logging.info("GET /results/%s  user=%s", tx_id, user_info)

    if not user_info or user_info["role"] not in ("Administrator", "Agent"):
        return jsonify({"error": "Unauthorized"}), 403

    cursor.execute("SELECT * FROM results WHERE transaction_id=?", (tx_id,))
    row = cursor.fetchone()
    if row:
        return jsonify({
            "transaction_id": row[1],
            "timestamp":      row[2],
            "is_fraudulent":  bool(row[3]),
            "confidence":     row[4]
        })
    return jsonify({"error": "Result not found"}), 404

if __name__ == "__main__":
    app.run(port=5001)
