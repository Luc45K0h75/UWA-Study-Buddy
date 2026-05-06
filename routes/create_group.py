from flask import Blueprint, render_template, request, redirect, url_for
from database import create_group_in_db

create_group_blueprint = Blueprint('create_group', __name__)

@create_group_blueprint.route("/create-group", methods=["GET", "POST"])
def create_group():
    if request.method == "POST":
        unit_code = request.form.get("unitCode")
        unit_name = request.form.get("unitName")
        topic = request.form.get("topic")
        description = request.form.get("description")
        materials = request.form.get("materials")
        time = request.form.get("time")
        location = request.form.get("location")
        members = request.form.get("members")

        # Send data to database.py to handle the actual insert
        create_group_in_db(unit_code, unit_name, topic, description, materials, time, location, members)

        return redirect(url_for("create_group.create_group"))

    return render_template("createGroup.html")