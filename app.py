from flask import Flask, render_template, request, redirect, url_for
import os # For the secret key
from config import Config # For the configuration of the app
from routes.index import index_blueprint # For the index file
from routes.viewGroups import view_groups_blueprint # For the view groups file
from routes.create_group import create_group_blueprint # For the create group file
from routes.addSession import add_session_blueprint # For the add session file
from routes.myGroups import my_groups_blueprint # For the my groups file
from extensions import db, migrate # For the database and migration
from datetime import datetime
import sqlalchemy as sa
from models import User, Unit, Groups, StudentGroups # importing database models

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY') or 'secret-key'
db.init_app(app)
migrate.init_app(app, db)

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

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        StudentID = int(request.form.get("student_id"))
        Firstname = request.form.get("firstname")
        Lastname = request.form.get("lastname")
        Username = request.form.get("username")
        Password = request.form.get("password") #password hashing will be required
        Course = request.form.get("course")
        Email = request.form.get("email")
        GraduationYear = request.form.get("graduation")
        birthday_string = request.form.get("birthday") #Obtaining the input birthday string
        Birthday = datetime.strptime(birthday_string, "%Y-%m-%d") if birthday_string else None #converting the birthday string into datetime format

        #Once information obtained, to create new profile, using the User Class
        new_profile_user = User(StudentID=StudentID, Firstname=Firstname, Lastname=Lastname, Username=Username, Password=Password, Course=Course, Email=Email, GraduationYear=GraduationYear, Birthday=Birthday)
        db.session.add(new_profile_user)
        db.session.commit()

        return redirect(url_for("login_page")) #once user is succcessfully signed up, they will be redirected to the login page
    return render_template("signup.html")

@app.route("/login-page", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        Username = request.form.get("username")
        Password = request.form.get("password")

        #Checking if the username and password exists in the db/if user exists
        check_user = User.query.filter_by(Username=Username, Password=Password).first()

        if check_user:
            return redirect(url_for("view_profile")) #or maybe homepage?
        else:
            return render_template("loginpage.html", error="Invalid Username or Password, please try again")
    return render_template("loginpage.html")

# Handles the View Profile page
@app.route("/view-profile")
def view_profile():
    # Temporary user until login is connected properly
    student_id = 12345678

    # Get the student's basic profile details
    user = db.session.execute(
        sa.select(
            User.StudentID,
            User.Username,
            User.Course,
            User.GraduationYear,
            User.Email
        ).where(User.StudentID == student_id)
    ).mappings().first()

    # Get up to 4 units connected to the student's groups
    preferred_units = db.session.execute(
        sa.select(Unit.UnitName)
        .distinct()
        .join(Groups, Unit.UnitID == Groups.UnitID)
        .join(StudentGroups, Groups.GroupID == StudentGroups.GroupID)
        .where(StudentGroups.StudentID == student_id)
        .limit(4)
    ).mappings().all()

    # Get up to 3 groups the student has joined
    joined_groups = db.session.execute(
        sa.select(
            Groups.GroupName,
            Unit.UnitName,
            Groups.Description
        )
        .join(Unit, Groups.UnitID == Unit.UnitID)
        .join(StudentGroups, Groups.GroupID == StudentGroups.GroupID)
        .where(StudentGroups.StudentID == student_id)
        .limit(3)
    ).mappings().all()

    # Simple stats for the profile page
    stats = {
        "groups_joined": len(joined_groups),
        "sessions_attended": 0,
        "favourite_unit": preferred_units[0]["UnitName"] if preferred_units else "No unit yet"
    }

    return render_template(
        "viewProfile.html",
        username=user["Username"] if user else "Student",
        user=user,
        preferred_units=preferred_units,
        joined_groups=joined_groups,
        stats=stats
    )

if __name__ == "__main__":
    app.run(debug=True)