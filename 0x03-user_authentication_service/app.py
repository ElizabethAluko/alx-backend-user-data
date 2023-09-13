#!/usr/bin/env python3
"""Application Module"""

from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route('/users', methods=['GET', 'POST'])
def users():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        # Register the user using AUTH.
        AUTH.register_user(email, password)

        # If successful, respond with the following json payload.
        response_data = {"email": email, "message": "user created"}
        return jsonify(response_data), 200
    except ValueError as e:
        # Catch the exception for duplicate email
        error_message = str(e)
        response_data = {"message": error_message}
        return jsonify(response_data), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
