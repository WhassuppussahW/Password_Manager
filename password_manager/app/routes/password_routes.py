from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.services.password_service import add_password, retrieve_password, delete_password, generate_random_password, retrieve_all_websites
import logging
from flask_login import login_required
import bleach 

password_bp = Blueprint("password", __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@password_bp.route("/add-password", methods=["GET", "POST"])
@login_required
def add_password_route():
    if request.method == "POST":
        website = bleach.clean(request.form.get("website"))
        password = request.form.get("password")
        master_password = bleach.clean(request.form.get("master_password"))
        
        if not website or not password or not master_password:
            flash("Website and password are required.", "error")
            username = session.get("username")
            return redirect(url_for("password.add_password_route", username=username))

        try:
            user_id = session.get("user_id")  # Retrieve user_id from the session THE USER ID IN SESSION IS IN HEX, NEED BACK TO BYTES TO RECOGNIZED IN DB
            if not user_id:
                flash("User is not logged in.", "error")
                return redirect(url_for("auth.login"))  # Redirect to login page if user_id is not found
            
            user_id_bytes = bytes.fromhex(user_id)
            add_password(user_id_bytes, master_password, website, password)
            flash("Password added successfully!", "success")
        except Exception as e:
            logging.error(f"Error adding password: {e}")  # Add logging for errors
            flash(f"Error: {e}", "error")
        return redirect(url_for("main.main_page"))

    return render_template("add_password.html")


@password_bp.route("/retrieve-password", methods=["GET", "POST"])
@login_required
def retrieve_password_route():
    if request.method == "GET":
        # Render the HTML page
        username = session.get("username")
        return render_template("retrieve.html", username=username)

    if request.method == "POST":
        try:
            data = request.get_json()
            logging.debug(f"Received POST data: {data}")

            website = bleach.clean(data.get("website"))
            master_password = bleach.clean(data.get("master_password"))

            if not website or not master_password:
                logging.error("Missing website or master_password")
                return jsonify({"error": "Website and master password are required."}), 400

            user_id = session.get("user_id")
            if not user_id:
                logging.error("User not logged in.")
                return jsonify({"error": "User not logged in."}), 401

            user_id_bytes = bytes.fromhex(user_id)
            password = retrieve_password(user_id_bytes, website, master_password)
            if password:
                logging.debug(f"Retrieved password: {password}")
                return jsonify({"password": password})
            logging.error("Password not found.")
            return jsonify({"error": "Password not found"}), 404
        except Exception as e:
            logging.exception("Exception occurred while retrieving password")
            return jsonify({"error": str(e)}), 500




@password_bp.route("/delete-password", methods=["GET", "POST"])
@login_required
def delete_password_route():
    username = session.get("username")
    if request.method == "POST":
        data = request.get_json()  # Accept JSON input
        website = bleach.clean(data.get("website"))
        if not website:
            flash("Website is required.", "error")
            return render_template("delete_password.html", username=username)
        try:
            user_id = session.get("user_id")  # Get user ID from session

            user_id_bytes = bytes.fromhex(user_id)
            delete_password(user_id_bytes, website)
            flash(f"Password for {website} deleted successfully.", "success")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("main.main_page"))
    return render_template("delete_password.html", username=username)


@password_bp.route("/generate-password", methods=["GET"])
def generate_password_route():
    length = request.args.get("length", default=16, type=int)  # Default to 16 if no length is specified
    if length < 4 or length > 64:  # Optional: Password length constraint (minimum 4, max 64)
        return jsonify({"error": "Password length must be between 4 and 64 characters"}), 400
    try:
        password = generate_random_password(length)  # Generate password based on requested length
        return jsonify({"password": password})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@password_bp.route("/get-websites", methods=["GET"])
def get_websites():
    try:
        user_id = session.get("user_id")  # Make sure the user_id is available in the session
        if not user_id:
            return jsonify({"error": "User not logged in."}), 401
        
        user_id_bytes = bytes.fromhex(user_id)
        websites = retrieve_all_websites(user_id_bytes)  # Implement this function in your service layer
        return jsonify({"websites": websites})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
