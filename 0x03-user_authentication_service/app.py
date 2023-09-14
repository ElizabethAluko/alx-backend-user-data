#!/usr/bin/env python3
"""Application Module"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    """Index Page"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route('/users', methods=['POST'])
def users():
    """Register a new user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        # Register the user using AUTH.
        AUTH.register_user(email, password)

        # If successful, respond with the following json payload.
        response_data = {"email": email, "message": "user created"}
        return jsonify(response_data), 200
    except ValueError:
        # Catch the exception for duplicate email
        response_data = {"message": "email already registered"}
        return jsonify(response_data), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Login function"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if login information is correct
        if not AUTH.valid_login(email, password):
            abort(401)   # Unauthorized

        # If login is correct, create a new session and store it as cookie.
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email,
                                          "message": "logged in"}))
        response.set_cookie("session_id", session_id)

        return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Delete stored session_id to logout the user"""

    if request.method == 'DELETE':
        session_id = request.cookies.get('session_id')

    try:
        # Find the user with the session id.
        user = AUTH.get_user_from_session_id(session_id)

        # Destoy the session_id
        AUTH.destroy_session(user.user_id)

        # Redirect to GET /
        return redirect('/')

    except ValueError:
        # If the user does not exist
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """Send the user profile kn GET request"""
    if request.method == 'GET':
        session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    
    if user:
        return jsonify({"email": user.email}), 200

    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
