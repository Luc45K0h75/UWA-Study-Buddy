from flask import Blueprint, render_template  # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from extensions import db
from models import Groups, StudentGroups, Role, Session
import sqlalchemy as sa
from flask_login import login_required, current_user #using the flask-login extension to maintain user login-session
from datetime import datetime

# Creates the blueprint to handle myGroups.html
my_groups_blueprint = Blueprint('my_groups', __name__)

#Paths to the page in the url browser
@my_groups_blueprint.route('/my-groups')
@login_required #ensuring user is logged in before they access this page
def my_groups():
    student_id = current_user.StudentID #removed placeholder. This now contains student id of the logged in user

    # Query to get groups the student has joined
    query = sa.select(StudentGroups.StudentID, StudentGroups.GroupID, Groups.GroupName, Groups.Description, Role.Type).join(Groups, StudentGroups.GroupID == Groups.GroupID).join(Role, StudentGroups.RoleID == Role.RoleID).where(StudentGroups.StudentID == student_id)
    studentGroups = db.session.execute(query).mappings().all()

    # Query to get all sessions linked to the student's joined groups
    session_rows = db.session.execute(
        sa.select(
            Session.GroupID,
            Session.Description,
            Session.SessionDateTime,
            Session.Location
        )
        .join(StudentGroups, Session.GroupID == StudentGroups.GroupID)
        .where(StudentGroups.StudentID == student_id)
        .order_by(Session.SessionDateTime.asc())
    ).mappings().all()

    # Build a dict mapping GroupID -> list of formatted sessions
    sessions_by_group = {}
    for s in session_rows:
        gid = s['GroupID']
        if gid not in sessions_by_group:
            sessions_by_group[gid] = []
        sessions_by_group[gid].append({
            "Description": s['Description'],
            "Location": s['Location'] or "TBD",
            "SessionDateTime": datetime.fromtimestamp(s['SessionDateTime']).strftime("%d %b %Y, %I:%M %p")
        })

    return render_template('myGroups.html', studentGroups=studentGroups, sessions_by_group=sessions_by_group)