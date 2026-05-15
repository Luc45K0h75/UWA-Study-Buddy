from flask import Flask, render_template, request, redirect, url_for
import os # For the secret key
from config import Config # For the configuration of the app
from routes.index import index_blueprint # For the index file
from routes.viewGroups import view_groups_blueprint # For the view groups file
from routes.create_group import create_group_blueprint # For the create group file
from routes.addSession import add_session_blueprint # For the add session file
from routes.myGroups import my_groups_blueprint # For the my groups file
from routes.viewProfile import view_profile_blueprint # For the view profile file
from routes.signup import sign_up_blueprint # For the signup file
from routes.loginPage import login_page_blueprint # For the login page file
from routes.logout import logout_blueprint # For the logout file
from extensions import db, migrate # For the database and migration
from datetime import datetime
import sqlalchemy as sa
from models import User, Unit, Groups, StudentGroups # importing database models
from flask_login import LoginManager, login_user, logout_user, current_user, login_required #this is for the login route/to ensure user remains logged in when navigating pages (login session)
from werkzeug.security import generate_password_hash, check_password_hash #to hash the password when users sign up, for security
from flask_wtf.csrf import CSRFProtect  # import CSRF protection

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY') or 'secret-key'
db.init_app(app)
migrate.init_app(app, db)

# Disable CSRF protection during testing to avoid issues with form submissions in tests
app.config['WTF_CSRF_ENABLED'] = os.environ.get('TESTING') != 'True'

csrf = CSRFProtect(app)  # enable CSRF protection across all POST forms


#Initialising Login Manager. This is the controller of the login session system.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page.login_page"

# When Syifa and I create our dates, they were stored as different data types
@app.template_filter('dateconverter')
def format_datetime(value):
    return datetime.fromtimestamp(int(value)).strftime('%d %b %Y %I:%M %p')

# Blueprints for different pages of the website
app.register_blueprint(index_blueprint)
app.register_blueprint(view_groups_blueprint)
app.register_blueprint(create_group_blueprint)
app.register_blueprint(add_session_blueprint)
app.register_blueprint(my_groups_blueprint)
app.register_blueprint(view_profile_blueprint)
app.register_blueprint(sign_up_blueprint)
app.register_blueprint(login_page_blueprint)
app.register_blueprint(logout_blueprint)  # logout is handled here via blueprint only

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)