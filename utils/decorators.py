from functools import wraps
from flask import session, redirect, url_for, jsonify, request
from utils.jwt_utils import verify_token


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = session.get("token")
        if not token:
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "message": "Unauthorized"}), 401
            return redirect(url_for("auth.login_page"))

        payload = verify_token(token)
        if not payload:
            session.clear()
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "message": "Session expired"}), 401
            return redirect(url_for("auth.login_page"))

        request.user = payload
        return f(*args, **kwargs)
    return wrapper


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = session.get("token")
            if not token:
                if request.path.startswith("/api/"):
                    return jsonify({"success": False, "message": "Unauthorized"}), 401
                return redirect(url_for("auth.login_page"))

            payload = verify_token(token)
            if not payload:
                session.clear()
                if request.path.startswith("/api/"):
                    return jsonify({"success": False, "message": "Session expired"}), 401
                return redirect(url_for("auth.login_page"))

            if payload.get("role") != required_role:
                if request.path.startswith("/api/"):
                    return jsonify({"success": False, "message": "Forbidden"}), 403
                return redirect(url_for("auth.login_page"))

            request.user = payload
            return f(*args, **kwargs)
        return wrapper
    return decorator