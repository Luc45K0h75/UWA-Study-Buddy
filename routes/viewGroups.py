from flask import Blueprint, render_template, request # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from extensions import db
from datetime import datetime # For use in the query
from models import Groups, Unit, GroupType, Faculty
import sqlalchemy as sa


# Creates the blueprint to handle viewGroups.html
view_groups_blueprint = Blueprint('view_groups', __name__)

#Paths to the page in the url browser
@view_groups_blueprint.route('/view-groups')

def view_groups():
    # First is to get all of the filters that allow for you to search for a grouo

    # Get all faculties for the dropdown
    faculties = db.session.execute(
        sa.select(Faculty.FacultyID, Faculty.Name)
    ).mappings().all()

    # Get all units for the dropdown
    units = db.session.execute(
        sa.select(Unit.UnitID, Unit.UnitName)
    ).mappings().all()

    # Get all group types for the dropdown
    groupTypes = db.session.execute(
        sa.select(GroupType.GroupTypeID, GroupType.Type)
    ).mappings().all()

    faculty = request.args.get('faculty')
    unit = request.args.get('unit')
    group_type = request.args.get('group_type')

    query = sa.select(Groups.GroupID, Groups.GroupName, Groups.Description).join(Unit, Groups.UnitID == Unit.UnitID)

    # Apply filters to the query based on user selection
    if faculty:
        query = query.where(Unit.FacultyID == faculty)

    if unit:
        query = query.where(Groups.UnitID == unit)

    if group_type:
        query = query.where(Groups.GroupTypeID == group_type)

    groups = db.session.execute(query).mappings().all()


    return render_template('viewGroups.html', 
        faculties=faculties, 
        units=units, 
        groupTypes=groupTypes,
        groups=groups
    )

    


