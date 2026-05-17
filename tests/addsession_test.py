import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db
from models import User, Groups, Unit, StudentGroups
from datetime import datetime
from werkzeug.security import generate_password_hash


class AddSessionTest(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            WTF_CSRF_ENABLED=False
        )
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        #Resets database before each test
        db.session.remove()
        db.drop_all()
        db.create_all()

        # Create a user, as page requires a logged in user
        test_user = User(
            StudentID="23456788",
            Firstname="Mara",
            Lastname="Smith",
            Username="maras",
            Password=generate_password_hash("mara123"), 
            Course="Computer Science",
            Email="mara245@gmail.com",
            GraduationYear="2028",
            Birthday="2008-02-03"
        )

        db.session.add(test_user)
        db.session.commit()

        #Creating a test unit and group
        test_unit = Unit(
            UnitID=1,
            UnitName="Agile Web Dev",
            UnitCode="CITS3403"
        )

        db.session.add(test_unit)
        db.session.commit()

        test_group = Groups(
            GroupName="Project Study Group",
            UnitID=1,
            GroupTypeID=1,
            CreationDate=datetime(2026, 2, 3),
            Description="Study group for group project",
            MaxMembers=10
        )

        db.session.add(test_group)
        db.session.commit()

        # Adding a member user as admin
        test_member = StudentGroups(
            StudentID="23456788",
            GroupID=1,
            RoleID=2
        )

        db.session.add(test_member)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #logs in the test user, as page requires a logged in user
    def login(self):
        self.client.post(
            "/login-page",
            data={
                "username": "maras",
                "password": "mara123"
            },
            follow_redirects=True
        )

    #checking that a a valid adding session works
    def test_add_session_valid(self):
        self.login()
        response = self.client.post(
            "/add-session",
            data={
                "group_id": "1",
                "description": "Project Meeting 1",
                "date": "2026-05-03",
                "time": "11:00",
                "location": "Reid Library"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Session added successfully!", response.data)

    # Checking when user is not admin, it should not allow them to add a session
    def test_add_session_not_authorized(self):
        self.login()
        # Updating user to non-admin
        membership = StudentGroups.query.filter_by(
            StudentID="23456788",
            GroupID=1
        ).first()

        membership.RoleID = 1  #Changing the role ID
        db.session.commit()

        response = self.client.post(
            "/add-session",
            data={
                "group_id": "1",
                "description": "Project meeting 1",
                "date": "2026-05-03",
                "time": "11:00",
                "location": "Reid Library"
            },
            follow_redirects=True
        )

        self.assertIn(
            b"You are not authorized to manage sessions",
            response.data
        )

    #As page requires user to be logged in, Checking that a guest user will then be redirected to login first
    def test_addsession_guest(self):
        response = self.client.get("/view-profile", follow_redirects=False)

        # directed to login if user is not logged in.
        self.assertEqual(response.status_code, 302)
        self.assertIn(b"/login", response.data.lower())

if __name__ == "__main__":
    unittest.main()