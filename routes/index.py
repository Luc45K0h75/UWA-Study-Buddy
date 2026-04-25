# This is the code for the home page
from flask import Blueprint, render_template # Our group chose to use blueprints because we could keep the python for each page separate allowing us to avoide merge conflicts
from database import get_data # Imports our python from database.py to get the file
from datetime import datetime # For use in the query

# Creates the blueprint to handle index.html
index_blueprint = Blueprint('index', __name__)

#Paths to the page in the url browser
@index_blueprint.route('/')
@index_blueprint.route('/index')

def index():
    connection = get_data() # Path to database
    student_id = 12345678 # Dummy to be changed later

    # Get username
    user = connection.execute("SELECT Username FROM User WHERE StudentID = ?", (student_id,)).fetchone()

    # Query to get upcoming events
    upcoming_events = connection.execute("""
        SELECT st.Name, s.SessionDateTime AS Date, g.GroupName, s.Description, s.Location, u.UnitName
        FROM Session s
        JOIN Groups g ON s.GroupID = g.GroupID
        JOIN SessionType st ON s.SessionTypeID = st.SessionTypeID
        JOIN Unit u ON g.UnitID = u.UnitID
        JOIN StudentGroups sg ON sg.GroupID = g.GroupID
        WHERE sg.StudentID = ? AND s.SessionDateTime >= ?
        ORDER BY s.SessionDateTime ASC
        LIMIT 3
    """, (student_id, int(datetime.now().timestamp()))).fetchall() # The date time function prevents events already being from being shown

    # Query to find 3 most recently created groups
    new_groups = connection.execute("""
        SELECT g.GroupName, u.UnitName, g.Description, gt.Type AS 'GroupType'
        FROM Groups g
        JOIN Unit u ON g.UnitID = u.UnitID
        JOIN GroupType gt ON g.GroupTypeID = gt.GroupTypeID
        ORDER BY (g.CreationDate) DESC
        LIMIT 3                        
    """).fetchall()

    print(new_groups)
    connection.close()

    # Returns rendered template for use in html
    return render_template("index.html", username=user["Username"] if user else "Student", upcoming_events=upcoming_events, new_groups=new_groups)
    