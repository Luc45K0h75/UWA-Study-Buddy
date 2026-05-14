from datetime import datetime
from extensions import db
from models import Unit, Groups, Session, StudentGroups
from flask import session
from flask_login import current_user

# Receives the create group form data from routes/create_group.py
# Inserts the data into the Unit, Groups, and Session tables
def create_group_in_db(unit_code, unit_name, faculty_id, topic, description, materials, date, time, location, members):
    
    # Check if the unit already exists in the database. If not, create a new unit entry so we don't store duplicates
    unit = Unit.query.filter_by(UnitCode=unit_code).first()
    if not unit:
        unit = Unit(
            UnitCode=unit_code,
            UnitName=unit_name,
            FacultyID=faculty_id
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

    # Add the creator as admin (RoleID=1) to the group
    # double check when the actual login implemented

    if current_user.is_authenticated: # Only add to StudentGroups if the user is logged in
        student_id = current_user.StudentID
        creator = StudentGroups(
            StudentID=student_id,
            GroupID=new_group.GroupID,
            RoleID=2        # RoleID=2 is admin
        )
        db.session.add(creator)

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

        # Store as UNIX timestamp (integer)
        unix_timestamp = int(session_datetime.timestamp())

        new_session = Session(
            GroupID=new_group.GroupID,
            SessionTypeID=1,                # Default SessionTypeID for now
            Description=materials or "",    # Use materials as the session description
            SessionDateTime=unix_timestamp,
            Location=location or ""         # Use empty string if no location given
        )
        db.session.add(new_session)

    # Commit everything to the database in one go
    db.session.commit()