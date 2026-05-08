# This code simply imports our database so that we don't have to import it every time

# Imports
import sqlite3 # We are using sqlite3 for our project's database
import os  # Used to get the path to the database
from datetime import datetime
from extensions import db
from models import Unit, Groups, Session

def get_data():
    path = os.path.dirname(os.path.abspath(__file__)) # Gets the path to where the database is stored
    database = os.path.join(path, "StudyBuddy.db") # This then retrieves the file path based on the path we found befor   
    connection = sqlite3.connect(database) # Creatse a connection to the database
    connection.row_factory = sqlite3.Row # Converts the data so it can be accessed by columns not just index
    return connection 


# Receives the create group form data from routes/create_group.py
# Inserts the data into the Unit, Groups, and Session tables
def create_group_in_db(unit_code, unit_name, topic, description, materials, date, time, location, members):
    
    # Check if the unit already exists in the database. If not, create a new unit entry so we don't store duplicates
    unit = Unit.query.filter_by(UnitCode=unit_code).first()
    if not unit:
        unit = Unit(
            UnitCode=unit_code,
            UnitName=unit_name,
            # FacultyID
        )
        db.session.add(unit)
        db.session.flush()  # Flush so we can access the new UnitID before committing

    # Create the new study group
    new_group = Groups(
        UnitID=unit.UnitID,
        GroupTypeID=1,          # Default GroupTypeID for now, can be updated later
        GroupName=topic,
        Description=description or "",  # Use empty string if no description given
        CreationDate=datetime.now(),
        MaxMembers=int(members) if members else None  # Convert to int, or None if not provided
    )
    db.session.add(new_group)
    db.session.flush()  # Flush so we can access the new GroupID before committing

    # Create the study session if a date was provided
    # A session is the actual scheduled meeting/event for the group
    if date:
        # Combine the separate date and time fields into one datetime object
        if time:
            # If both date and time are given, combine them
            session_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        else:
            # If only date is given, default time to midnight
            session_datetime = datetime.strptime(date, "%Y-%m-%d")

        new_session = Session(
            GroupID=new_group.GroupID,
            SessionTypeID=1,                # Default SessionTypeID for now
            Description=materials or "",    # Use materials as the session description
            SessionDateTime=session_datetime,
            Location=location or ""         # Use empty string if no location given
        )
        db.session.add(new_session)

    # Commit everything to the database in one go
    db.session.commit()