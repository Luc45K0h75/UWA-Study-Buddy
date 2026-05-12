from flask import Blueprint, render_template, request, redirect, url_for
from helpers import create_group_in_db

# Creates the blueprint to handle createGroup.html
create_group_blueprint = Blueprint('create_group', __name__)

# Handles both loading the page (GET) and submitting the form (POST)
@create_group_blueprint.route("/create-group", methods=["GET", "POST"])
def create_group():
    # If the form is submitted, read the values entered by the user
    if request.method == "POST":
        unit_code = request.form.get("unitCode")
        unit_name = request.form.get("unitName")
        faculty = request.form.get("faculty")
        topic = request.form.get("topic")
        description = request.form.get("description")
        materials = request.form.get("materials")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        members = request.form.get("members")

        # Send data to database.py to handle the actual insert
        create_group_in_db(unit_code, unit_name, faculty, topic, description, materials, date, time, location, members)

        # After processing the form, redirect back to the create group page
        return redirect(url_for("create_group.create_group"))

    # If the user is just visiting the page (GET), show the empty form
    return render_template("createGroup.html")