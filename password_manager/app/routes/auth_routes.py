from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import sign_in_user, login_user, get_user_by_id
from flask_login import logout_user
from flask_login import login_user as flask_login_user
from app.services.auth_service import login_user
import bleach


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def home():
    return render_template("sign-log-in.html")

@auth_bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = bleach.clean(request.form["username"])
        password = bleach.clean(request.form["password"])
        confirm_password = bleach.clean(request.form["confirm_password"])
        
        if password == confirm_password:
            success = sign_in_user(username, password)
            if success:
                # Automatically log in the user
                user = login_user(username, password)
                if user:
                    flask_login_user(user) # Log the user in with Flask-Login
                    session["user_id"] = user.id.hex() if isinstance(user.id, bytes) else user.id # Convert bytes to hex string if needed
                    session["username"] = user.username # Storing the username in session ["username"]
                    session.permanent = True  # Mark the session as permanent
                    flash("Sign-in successful! You are now logged in.", "success")
                    return redirect(url_for("main.main_page"))
        else:
            flash("Passwords do not match, please try again.", "error")
    
    return render_template("sign-log-in.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = bleach.clean(request.form.get("username"))
        password = bleach.clean(request.form.get("password"))
        
        # Authenticate user (this function should validate the username and password)
        user = login_user(username, password)
        
        if user:
            flask_login_user(user) # Log the user in with Flask-Login
            session["user_id"] = user.id.hex() if isinstance(user.id, bytes) else user.id # Convert bytes to hex string
            session["username"] = user.username # Storing the username in session ["username"]
            session.permanent = True # Mark the session as permanent
            flash("Login successful!", "success")
            return redirect(url_for("main.main_page"))  # Redirect to the main page after successful login
        else:
            flash("Invalid credentials, please try again.", "error")
    
    return render_template("sign-log-in.html")

@auth_bp.route("/logout") 
def logout(): 
    logout_user() 
    flash("You have been logged out.", "info") 
    return redirect(url_for("auth.login"))

"""
@auth_bp.route("/profile")
def profile():
    # Access user_id from the session
    user_id = session.get("user_id")  # Get the user_id, returns None if the user is not logged in
    
    if not user_id:
        flash("You must log in to view your profile.", "error")
        return redirect(url_for("auth.login"))  # Corrected blueprint name
    
    # Proceed to retrieve user information or display the profile
    user = get_user_by_id(user_id)  # Assuming you have a function to fetch user by ID
    return render_template("profile.html", user=user)
"""