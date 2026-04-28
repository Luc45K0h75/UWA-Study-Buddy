from flask import Flask, render_template, request, redirect, url_for
import os # For the secret key
from routes.index import index_blueprint # For the index file
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'secret-key'

# Converts date from datetime (which is what it is stored as) to an actual string date
@app.template_filter('dateconverter')
def format_datetime(value):
    return datetime.fromtimestamp(value).strftime('%d %b %Y %I:%M %p')

# Register blueprint provided in index.py
app.register_blueprint(index_blueprint)

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

@app.route("/view-groups")
def view_groups():
    return render_template("viewGroups.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/view-profile")
def view_profile():
    return render_template("viewProfile.html")

if __name__ == "__main__":
    app.run(debug=True)