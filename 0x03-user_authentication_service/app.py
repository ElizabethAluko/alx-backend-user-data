#!/usr/bin/env python3
"""Application Module"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
