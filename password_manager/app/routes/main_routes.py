from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from flask_login import login_required

main_bp = Blueprint("main", __name__)

@main_bp.route("/main-page", methods=["GET"])
@login_required
def main_page():
    username = session.get("username") # Get the username from the session
    return render_template("main_page.html", username=username)

@main_bp.route("/logout", methods=["POST"])
def logout():
    # Clear session and redirect to login
    session.clear()
    return redirect(url_for("auth.home"))

@main_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200
