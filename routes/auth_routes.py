from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from services.auth_service import authenticate
from utils.validators import is_empty

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def login_page():
    if session.get("token"):
        role = session.get("role")
        if role == "owner":
            return redirect(url_for("owner.dashboard"))
        elif role == "renter":
            return redirect(url_for("renter.view"))
    return render_template("auth/login.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or request.form
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if is_empty(username) or is_empty(password):
        return jsonify({"success": False, "message": "Username and password required"}), 400

    result = authenticate(username, password)
    if not result:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    session["token"] = result["token"]
    session["role"] = result["role"]
    session["username"] = result["username"]
    session["room_id"] = result["room_id"]

    redirect_url = url_for("owner.dashboard") if result["role"] == "owner" else url_for("renter.view")

    return jsonify({
        "success": True,
        "message": "Login successful",
        "role": result["role"],
        "redirect": redirect_url
    })


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))