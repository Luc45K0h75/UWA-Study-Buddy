import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db
from models import User, Groups
from werkzeug.security import generate_password_hash

class CreateGroupTest(unittest.TestCase):
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
            StudentID="23456789",
            Firstname="Mary",
            Lastname="Smith",
            Username="marys",
            Password=generate_password_hash("mary123"), 
            Course="Computer Science",
            Email="mary245@gmail.com",
            GraduationYear="2028",
            Birthday="2008-02-05"
        )

        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self): #logs in the test user, as page requires a logged in user
        self.client.post(
            "/login-page",
            data={
                "username": "marys",
                "password": "mary123"
            },
            follow_redirects=True
        )
    #attempts and tests at creating a study group
    def test_create_group(self):
        self.login()
        response = self.client.post(
            "/create-group",
            data={
                "unitCode": "C3403",
                "unitName": "Agile Web Development",
                "faculty": "Computer Science",
                "topic": "Group Project Study",
                "description": "Study group for group project",
                "materials": "Laptop",
                "date": "2026-05-03",
                "time": "10:00",
                "location": "Reid Library",
                "members": "4"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
    
    #Testing an empty creation form
    def test_empty_form(self):
        self.login()
        response = self.client.post(
            "/create-group",
            data={
                "unitCode": "",
                "unitName": "",
                "faculty": "",
                "topic": "",
                "description": "",
                "materials": "",
                "date": "",
                "time": "",
                "location": "",
                "members": ""
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    #Testing if user somehow bypasses Javascript validation, backend does not crash. Test is done by using an invalid student code and member number.
    def test_js_bypass_invalid_unit_code(self):
        self.login()
        response = self.client.post(
            "/create-group",
            data={
                "unitCode": "cit", #invalid
                "unitName": "Agile Web Development",
                "faculty": "Computer Science",
                "topic": "Group Project Study",
                "description": "Study group for group project",
                "materials": "Laptop",
                "date": "2026-05-03",
                "time": "10:00",
                "location": "Reid Library",
                "members": "0" #invalid
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    #As page requires user to be logged in, Checking that a guest user will then be redirected to login first
    def test_creategroup_guest(self):
        response = self.client.get("/view-profile", follow_redirects=False)

        # directed to login if user is not logged in.
        self.assertEqual(response.status_code, 302)
        self.assertIn(b"/login", response.data.lower())

if __name__ == "__main__":
    unittest.main()