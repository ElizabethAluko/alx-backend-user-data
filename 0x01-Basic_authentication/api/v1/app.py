#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv("AUTH_TYPE", default=None)

if auth:
    from api.v1.auth.auth import Auth

    auth = Auth()

excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']


@app.before_request
def before_request():
    """
    Handle authentication and authorization before each request.
    """
    # Check if auth is None
    if auth is None:
        return

    # Check if the request path is in the excluded paths
    if request.path in excluded_paths:
        return

    # Check if Authorization header is present
    if auth.authorization_header(request) is None:
        abort(401)  # Unauthorized

    # Check if current_user returns None
    if auth.current_user(request) is None:
        abort(403)  # Forbidden


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Access denied"""
    return jsonify({
        "error": "Unauthorized"
        }), 401


@app.errorhandler(403)
def forbidden(error):
    """Forbidden request"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
