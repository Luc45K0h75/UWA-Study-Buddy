# This is the code for the home page
from flask import Blueprint, render_template # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from datetime import datetime # For use in the query
from models import User, Session, Groups, SessionType, Unit, StudentGroups, GroupType
from extensions import db
import sqlalchemy as sa

# Creates the blueprint to handle index.html
index_blueprint = Blueprint('index', __name__)

#Paths to the page in the url browser
@index_blueprint.route('/')
@index_blueprint.route('/index')

def index():
    student_id = 12345678 # Dummy to be changed later

    # Get username
    user = db.session.get(User, student_id)
    username = user.Username if user else "Student"

    now = int(datetime.now().timestamp())

    # Query to get upcoming events
    upcoming_events = db.session.execute(
        sa.select(
            Session.SessionDateTime,
            Session.Description,
            Session.Location,
            SessionType.Name,
            Groups.GroupName,
            Unit.UnitName
        )
        .join(Groups, Session.GroupID == Groups.GroupID)
        .join(SessionType, Session.SessionTypeID == SessionType.SessionTypeID)
        .join(Unit, Groups.UnitID == Unit.UnitID)
        .join(StudentGroups, StudentGroups.GroupID == Groups.GroupID)
        .where(
            StudentGroups.StudentID == student_id,
            Session.SessionDateTime >= now
        )
        .order_by(Session.SessionDateTime.asc())
        .limit(3)
    ).mappings().all()
    # Query to find 3 most recently created groups
    new_groups = db.session.execute(
        sa.select(
            Groups.GroupName,
            Groups.Description,
            GroupType.Type.label('GroupType'),
            Unit.UnitName
        )
        .join(Unit, Groups.UnitID == Unit.UnitID)
        .join(GroupType, Groups.GroupTypeID == GroupType.GroupTypeID)
        .order_by(Groups.CreationDate.desc())
        .limit(3)
    ).mappings().all()

    # Returns rendered template for use in html
    return render_template("index.html", username=username, upcoming_events=upcoming_events, new_groups=new_groups)
    