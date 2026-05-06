from flask import Flask, render_template, request, redirect, url_for
import os # For the secret key
from config import Config # For the configuration of the app
from routes.index import index_blueprint # For the index file
from routes.viewGroups import view_groups_blueprint # For the view groups file
from extensions import db, migrate # For the database and migration
from datetime import datetime
from models import User #importing the user class from models.py

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY') or 'secret-key'
db.init_app(app)
migrate.init_app(app, db)

# Converts date from datetime (which is what it is stored as) to an actual string date
@app.template_filter('dateconverter')
def format_datetime(value):
    return datetime.fromtimestamp(value).strftime('%d %b %Y %I:%M %p')

# Blueprints for different pages of the website
app.register_blueprint(index_blueprint)
app.register_blueprint(view_groups_blueprint)

# Handles the Create Group page and receives submitted form data
@app.route("/create-group", methods=["GET", "POST"])
def create_group():
    # If the form is submitted, get the values entered by the user
    if request.method == "POST":
        unit_code = request.form.get("unitCode")
        unit_name = request.form.get("unitName")
        topic = request.form.get("topic")
        description = request.form.get("description")
        materials = request.form.get("materials")
        time = request.form.get("time")
        location = request.form.get("location")
        members = request.form.get("members")

        print("New create group form submitted:")
        print("Unit Code:", unit_code)
        print("Unit Name:", unit_name)
        print("Topic:", topic)
        print("Description:", description)
        print("Materials:", materials)
        print("Time:", time)
        print("Location:", location)
        print("Maximum Members:", members)

        return redirect(url_for("create_group"))
    return render_template("createGroup.html")

@app.route("/my-groups")
def my_groups():
    return render_template("myGroups.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/sign-up",methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        StudentID = int(request.form.get("student_id"))
        Firstname = request.form.get("firstname")
        Lastname =  request.form.get("lastname")
        Username =  request.form.get("username")
        Password = request.form.get("password") #password hashing will be required
        Course = request.form.get("course")
        Email = request.form.get("email")
        GraduationYear = request.form.get("graduation")
        birthday_string = request.form.get("birthday") #Obtaining the input birthday string
        Birthday = datetime.strptime(birthday_string, %Y-%m-%d) #converting the birtday string into datetime format

        #Once information obtained, to create new profile, using the User Class
        new_profile_user = User ( StudentID = StudentID, Firstname = Firstname, Lastname = Lastname, Username = Username, Password = Password, Course = Course, Email = Email, GraduationYear = GraduationYear, Birthday = Birthday)
        db.session.add(new_profile_user)
        db.session.commit()

        return redirect(url_for("login_page")) #once user is succcessfully signed up, they will be redirected to the login page
    return render_template("signup.html")

@app.route("/login-page", methods=["GET", "POST"])
def login_page():
    if request.method == "POST"
        Username =  request.form.get("username")
        Password = request.form.get("password") 
    
        #Checking if the username and password exists in the db/if user exists
        check_username = User.query.filter_by(Username=Username).first() #checks User db if this username exists
        check_password = User.query.filter_by(Password=Password).first() ##checks User db if this password exists

        if Username == check_username and Password = check_password:
            return redirect(url_for("view_profile")) #or maybe homepage?
        else:
            render_template("loginpage.html", error= "Invalid Username or Password, please try again")
    return render_template("loginpage.html")

@app.route("/view-profile")
def view_profile():
    return render_template("viewProfile.html")

if __name__ == "__main__":
    app.run(debug=True)