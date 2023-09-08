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
auth = getenv("AUTH_TYPE", default=None)


if auth:
    if auth.lower() == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()
else:
    auth = None


@app.before_request
def before_request():
    """
    Handle authentication and authorization before each request.
    """
    if auth is None:
        return

    # List of paths that do not require authentication
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    if request.path not in excluded_paths:
        if auth.require_auth(request.path, excluded_paths):
            authorization_header = auth.authorization_header(request)
            request.current_user = auth.current_user(request)

            if authorization_header is None:
                # Unauthorized (401)
                abort(401)

            if current_user is None:
                # Forbidden (403)
                abort(403)


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
