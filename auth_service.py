# -*- coding: utf-8 -*-
# Authentication Service
from flask import Flask, request, jsonify
import secrets, base64, logging

app = Flask(__name__)
logging.basicConfig(filename="auth_service.log", level=logging.DEBUG)

# In‑memory users
users = {
    "admin":     {"password": "adminpass",     "role": "Administrator"},
    "secretary": {"password": "secretarypass", "role": "Secretary"},
    "agent":     {"password": "agentpass",     "role": "Agent"},
}

tokens = {}  # in‑memory token store

# ---------- LOGIN ----------
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = users.get(data.get("username"))
    if user and user["password"] == data.get("password"):
        raw   = f'{data["username"]}:{secrets.token_urlsafe()}'
        token = base64.b64encode(raw.encode()).decode()
        tokens[token] = {"username": data["username"], "role": user["role"]}
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

# ---------- VERIFY ----------
@app.route("/auth/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization", "").strip().strip('"')
    if token in tokens:
        return jsonify(tokens[token])
    return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(port=5000)
