from flask import Blueprint, render_template, request, flash, url_for, redirect  # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from models import User
from werkzeug.security import check_password_hash # For checking the hashed password
from flask_login import login_user # For logging in the user after successful login

# Creates the blueprint to handle loginpage.html
login_page_blueprint = Blueprint('login_page', __name__)

# Paths to the page in the url browser
@login_page_blueprint.route("/login-page", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        Username = request.form.get("username")
        Password = request.form.get("password")

        #Checking if the username exists in the db/if user exists
        check_user = User.query.filter_by(Username=Username).first() #as passwords are hashed, user.query.filter will no longer work to check password


        if check_user and check_password_hash(check_user.Password, Password): 
            login_user(check_user)
            return redirect(url_for("view_profile.view_profile"))
        else:
            return render_template("loginpage.html", error="Invalid Username or Password, please try again")
    return render_template("loginpage.html")