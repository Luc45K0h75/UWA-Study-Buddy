from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Groups, Session, Unit, StudentGroups
from datetime import datetime
import sqlalchemy as sa
from flask_login import login_required, current_user

# Creates the blueprint to handle addSession.html
add_session_blueprint = Blueprint('add_session', __name__)

@add_session_blueprint.route("/add-session", methods=["GET", "POST"])
@login_required
def add_session():
    if request.method == "POST":
        group_id = request.form.get("group_id")
        description = request.form.get("description")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")

        # Authorization check — only admins (RoleID=2) of the selected group can add sessions
        membership = db.session.execute(
            sa.select(StudentGroups)
            .where(
                StudentGroups.StudentID == current_user.StudentID,
                StudentGroups.GroupID == group_id,
                StudentGroups.RoleID == 2  # 2 = Admin
            )
        ).first()

        if not membership:
            flash("You are not authorized to manage sessions for this group.")
            return redirect(url_for("add_session.add_session"))

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

        flash("Session added successfully!")
        return redirect(url_for("add_session.add_session"))

    # On GET, fetch only groups where the current user is an admin (RoleID=2)
    # FIX: Join Unit to get UnitCode, and filter by admin role so dropdown only shows
    #      groups the user can actually manage
    groups = db.session.execute(
        sa.select(
            Groups.GroupID,
            Groups.GroupName,
            Unit.UnitCode
        )
        .join(Unit, Groups.UnitID == Unit.UnitID)
        .join(StudentGroups, Groups.GroupID == StudentGroups.GroupID)
        .where(
            StudentGroups.StudentID == current_user.StudentID,
            StudentGroups.RoleID == 2  # Only groups where user is admin
        )
    ).mappings().all()

    return render_template("addSession.html", groups=groups)