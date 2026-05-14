from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Groups, Session
from datetime import datetime
import sqlalchemy as sa
from flask_login import login_required, current_user #using the flask-login extension to maintain user login-session

# Creates the blueprint to handle addSession.html
add_session_blueprint = Blueprint('add_session', __name__)

@add_session_blueprint.route("/add-session", methods=["GET", "POST"])
@login_required #ensuring user is logged in before they access this page
def add_session():
    if request.method == "POST":
        group_id = request.form.get("group_id")
        description = request.form.get("description")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")

        # Combine date and time then convert to UNIX timestamp
        if time:
            session_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        else:
            session_datetime = datetime.strptime(date, "%Y-%m-%d")

        unix_timestamp = int(session_datetime.timestamp())

        new_session = Session(
            GroupID=group_id,
            SessionTypeID=1,            # Default session type
            Description=description or "",
            SessionDateTime=unix_timestamp,
            Location=location or ""
        )
        db.session.add(new_session)
        db.session.commit()

        return redirect(url_for("add_session.add_session"))

    # On GET, fetch groups for the dropdown
    groups = db.session.execute(
        sa.select(Groups.GroupID, Groups.GroupName)
    ).mappings().all()

    return render_template("addSession.html", groups=groups)