from flask import Blueprint, render_template  # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from extensions import db
from models import Groups, StudentGroups, Role
import sqlalchemy as sa
from flask_login import login_required, current_user #using the flask-login extension to maintain user login-session

# Creates the blueprint to handle myGroups.html
my_groups_blueprint = Blueprint('my_groups', __name__)

#Paths to the page in the url browser
@my_groups_blueprint.route('/my-groups')
@login_required #ensuring user is logged in before they access this page
def my_groups():
    student_id = current_user.StudentID #removed placeholder. This now contains student id of the logged in user

    # Query to get groups the student has joined
    query = sa.select(StudentGroups.StudentID, StudentGroups.GroupID,Groups.GroupName, Groups.Description, Role.Type).join(Groups, StudentGroups.GroupID == Groups.GroupID).join(Role, StudentGroups.RoleID == Role.RoleID).where(StudentGroups.StudentID == student_id)
    studentGroups = db.session.execute(query).mappings().all()
    print(f"Found {len(studentGroups)} groups")
    for sg in studentGroups:
        print(dict(sg))
    return render_template('myGroups.html', studentGroups=studentGroups)
    