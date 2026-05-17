import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db
from models import User
from werkzeug.security import generate_password_hash


class LoginTest(unittest.TestCase):
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

        # Creating a test user, to test the login process
        test_user = User(
            StudentID="23456787",
            Firstname="Nia",
            Lastname="Smith",
            Username="nias",
            Password=generate_password_hash("nia123"), 
            Course="Computer Science",
            Email="nia245@gmail.com",
            GraduationYear="2028",
            Birthday="2008-02-04"
        )

        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #using the correct login information, to check that login succeeds
    def test_valid_login(self):
        response = self.client.post(
            "/login-page",
            data={
                "username": "nias",
                "password": "nia123"
            },
            follow_redirects=True
        )

        # Checking that it redirects to view profile page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"view-profile", response.data)

    #using the wrong login information, to check that login fails
    def test_invalid_login(self):
        response = self.client.post(
            "/login-page",
            data={
                "username": "niasz",
                "password": "nia124"
            },
            follow_redirects=True
        )

        self.assertIn(b"Invalid Username or Password", response.data)

if __name__ == "__main__":
    unittest.main()
