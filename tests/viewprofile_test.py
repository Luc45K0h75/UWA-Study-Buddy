import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

class ViewProfileTest(unittest.TestCase):
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

        #Create a user, as page requires a logged in user
        test_user = User(
            StudentID="23456788",
            Username="maras",
            Firstname="Mara",
            Lastname="Smith",
            Password=generate_password_hash("mara123"),
            Course="Computer Science",
            Email="mara245@gmail.com",
            GraduationYear="2028",
            Birthday="2008-02-03"
        )

        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self): #logs in the test user, as page requires a logged in user
        return self.client.post(
            "/login-page",
            data={
                "username": "maras",
                "password": "mara123"
            },
            follow_redirects=True
        )

    # Checking that profile loads when user is logged in
    def test_viewprofile_loggedin(self):
        self.login()
        response = self.client.get("/view-profile", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        self.assertIn(b"Student Profile", response.data)
        self.assertIn(b"Study Stats", response.data)

    #As page requires user to be logged in, Checking that a guest user will then be redirected to login first
    def test_viewprofile_guest(self):
        response = self.client.get("/view-profile", follow_redirects=False)

        # directed to login if user is not logged in.
        self.assertEqual(response.status_code, 302)
        self.assertIn(b"/login", response.data.lower())


if __name__ == "__main__":
    unittest.main()