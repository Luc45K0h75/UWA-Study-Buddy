from flask import Blueprint, render_template, request, flash, url_for, redirect  # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from models import User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required #this is for the login route/to ensure user remains logged in when navigating pages (login session)

# Creates the blueprint to handle logout
logout_blueprint = Blueprint('logout', __name__)

# Paths to the page in the url browser
@logout_blueprint.route("/logout") #this allows the user to be logged out, and then redirects to login page
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_page.login_page"))