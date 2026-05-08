from flask import Blueprint, render_template # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from database import get_data # Imports our python from database.py to get the file
from datetime import datetime # For use in the query
from models import Groups, Unit, GroupType, Faculty
import sqlalchemy as sa


# Creates the blueprint to handle viewGroups.html
view_groups_blueprint = Blueprint('view_groups', __name__)

#Paths to the page in the url browser
@view_groups_blueprint.route('/')
@view_groups_blueprint.route('/view-groups')

def view_groups():
    
    return render_template('viewGroups.html')
