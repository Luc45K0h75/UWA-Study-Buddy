from flask import Blueprint, render_template, request, flash, url_for, redirect  # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from extensions import db
from datetime import datetime # For use in the query
from models import User
from werkzeug.security import generate_password_hash # For hashing the password
from email_validator import validate_email, EmailNotValidError #To be used to check if user input email is valid

# Creates the blueprint to handle signup.html
sign_up_blueprint = Blueprint('sign_up', __name__)

# Paths to the page in the url browser
@sign_up_blueprint.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        StudentID = request.form.get("student_id")
        Firstname = request.form.get("firstname")
        Lastname = request.form.get("lastname")
        Username = request.form.get("username")
        raw_password = request.form.get("password") #obtaining the actual raw password, which will then be hashed
        Course = request.form.get("course")
        Email = request.form.get("email")
        GraduationYear = request.form.get("graduation")
        birthday_string = request.form.get("birthday") #Obtaining the input birthday string

        #Backend validation to ensure that all input signup fields are completed
        if not all([
            StudentID,
            Firstname,
            Lastname,
            Username,
            raw_password,
            Course,
            Email,
            GraduationYear,
            birthday_string
        ]):
            return render_template("signup.html", error= "Please complete all fields")
        
        #Checking that the student ID entered is numeric
        if not StudentID.isdigit():
            return render_template("signup.html", error= "Invalid Student ID")
        
        #Checking that the student ID is 8-digits long
        if len(StudentID) != 8:
            return render_template("signup.html", error= "Invalid: Student ID must be 8 digits")
        
        #Checking if the entered email is valid
        try:
            validate_email(Email)
        except EmailNotValidError:
            return render_template("signup.html", error= "Invalid email")

        #Checking if profile has already been created, usin the email provided
        check_email= if User.query.filter_by(Email=Email).first()
        if check_email:
             return render_template("signup.html", error="Email is already registered")
        
        #Checking if a profile has already been created, using the student id
        existing_studentid=User.query.filter_by(StudentID=StudentID).first()
        if existing_studentid:
            return render_template("signup.html", error= "Student ID already has been registered.")
        
        #Hashing the obtained password string:
        hashed_password = generate_password_hash(raw_password)

        #Ensuring the birthday String is converted correctly in datetime format. 
        try:
            Birthday = datetime.strptime(birthday_string, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return render_template("signup.html", error= "Invalid birthday format") #issues an error if users enter birthday in wrong format

        #Once information obtained, to create new profile, using the User Class
        new_profile_user = User(StudentID=StudentID, Firstname=Firstname, Lastname=Lastname, Username=Username, Password=hashed_password, Course=Course, Email=Email, GraduationYear=GraduationYear, Birthday=Birthday)
        db.session.add(new_profile_user)
        db.session.commit()

        #Creating a pop-up message, that tells user their account has been created and that they need to login. This will pop-up, after user has been redirected to login page
        flash("Account has been created successfully! Please login and welcome to UWA Study Buddy :)")

        return redirect(url_for("login_page.login_page")) #once user is succcessfully signed up, they will be redirected to the login page
    return render_template("signup.html")