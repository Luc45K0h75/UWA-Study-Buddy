from flask import Blueprint, render_template
from extensions import db
from models import Groups, StudentGroups, User, Unit, Session
import sqlalchemy as sa
from flask_login import login_required, current_user
from datetime import datetime

# Creates a blueprint for handling the View Profile page
view_profile_blueprint = Blueprint('view_profile', __name__)

# Paths to the page in the url browser
@view_profile_blueprint.route("/view-profile")
@login_required
def view_profile():
    student_id = current_user.StudentID

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

    # Get the next upcoming session linked to one of the student's joined groups
    current_time = int(datetime.now().timestamp())

    next_session_row = db.session.execute(
        sa.select(
            Session.SessionDateTime,
            Session.Location
        )
        .join(StudentGroups, Session.GroupID == StudentGroups.GroupID)
        .where(
            StudentGroups.StudentID == student_id,
            Session.SessionDateTime >= current_time
        )
        .order_by(Session.SessionDateTime)
        .limit(1)
    ).mappings().first()

    next_session = None
    if next_session_row:
        next_session = {
            "SessionDateTime": datetime.fromtimestamp(next_session_row["SessionDateTime"]).strftime("%d %b %Y, %I:%M %p"),
            "Location": next_session_row["Location"] if next_session_row["Location"] else "Not added yet"
        }

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
        stats=stats,
        next_session=next_session
    )