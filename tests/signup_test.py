import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db
from models import User
from werkzeug.security import check_password_hash

class SignupTest(unittest.TestCase):
    def setUp(self):
        app.config.from_mapping(
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #Testing that profile creation is successful when user signs up
    def test_successful_signup(self):
        response = self.client.post(
            "/sign-up",
            data={
                "student_id": "56789012",
                "firstname": "Mary",
                "lastname": "Smith",
                "username": "mary123",
                "password": "marytest",
                "course": "Computer Science",
                "email": "mary@gmail.com",
                "graduation": "2027",
                "birthday": "2006-02-03"
            },
            follow_redirects=True #used as signup page leads to the login page, after account registers successfully
        )

        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(Email="mary@gmail.com").first()

        self.assertIsNotNone(user)

    #Testing that password hashing works

    def test_passwordhash(self):
        self.client.post(
            "/sign-up",
            data={
                "student_id": "87654322",
                "firstname": "Matt",
                "lastname": "Jones",
                "username": "matt123",
                "password": "matttest",
                "course": "Software Engineering",
                "email": "matt123@gmail.com",
                "graduation": "2027",
                "birthday": "2006-04-08"
            },
            follow_redirects=True
        )
        user = User.query.filter_by(Email="matt123@gmail.com").first()

        self.assertIsNotNone(user)
        # Ensure password has been hashed and not stored in its orginal raw format
        self.assertNotEqual(user.Password, "matttest")

    #Testing that accounts can not be created with existing email
    def test_existing_email(self):
        test_user = User(
            StudentID="87654321",
            Firstname="Ben",
            Lastname="Jones",
            Username="ben123",
            Password="bentest",
            Course="Software Engineering",
            Email="ben123@gmail.com",
            GraduationYear="2028",
            Birthday="2008-04-08"
        )

        db.session.add(test_user)
        db.session.commit()

        # Using the duplicate email
        response = self.client.post(
            "/sign-up",
            data={
                "student_id": "77654321",
                "firstname": "Ben",
                "lastname": "Smith",
                "username": "ben456",
                "password": "ben123",
                "course": "Electrical Engineering",
                "email": "ben123@gmail.com",
                "graduation": "2027",
                "birthday": "2009-05-08"
            },
            follow_redirects=True
        )

        self.assertIn(
            b"Email is already registered",
            response.data
        )

    #Testing thats signup does not work with an invalid student id, less than 8 digits
    def test_invalid_student_id(self):
        response = self.client.post(
            "/sign-up",
            data={
                "student_id": "2587",
                "firstname": "Kara",
                "lastname": "Smith",
                "username": "karas",
                "password": "kara123",
                "course": "Computer Science",
                "email": "kara@gmail.com",
                "graduation": "2029",
                "birthday": "2007-01-07"
            },
            follow_redirects=True
        )

        self.assertIn(
            b"Invalid: Student ID must be 8 digits",
            response.data
        )


if __name__ == "__main__":
    unittest.main()