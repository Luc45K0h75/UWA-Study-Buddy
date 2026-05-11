from flask import Blueprint, render_template  # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from extensions import db
from models import Groups, StudentGroups, Role
import sqlalchemy as sa

# Creates the blueprint to handle myGroups.html
my_groups_blueprint = Blueprint('my_groups', __name__)

#Paths to the page in the url browser
@my_groups_blueprint.route('/my-groups')

def my_groups():
    student_id = 12345678

    # Query to get groups the student has joined
    query = sa.select(StudentGroups.StudentID, StudentGroups.GroupID,Groups.GroupName, Groups.Description, Role.Type).join(Groups, StudentGroups.GroupID == Groups.GroupID).join(Role, StudentGroups.RoleID == Role.RoleID).where(StudentGroups.StudentID == student_id)
    studentGroups = db.session.execute(query).mappings().all()
    print(f"Found {len(studentGroups)} groups")
    for sg in studentGroups:
        print(dict(sg))
    return render_template('myGroups.html', studentGroups=studentGroups)
    