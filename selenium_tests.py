# Selenium tests for the functionality of different parts of the website.
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Base URL for the Flask app
BASE_URL = 'http://127.0.0.1:5000'

class TestStudyBuddy(unittest.TestCase):
    # Setup method to initialize the WebDriver using ChromeDriver
    def setUp(self):
        self.driver = webdriver.Chrome()  
        self.driver.get(BASE_URL)

    # Teardown method to quit the WebDriver after each test
    def tearDown(self):
        self.driver.quit()

    # Test homepage loads correctly
    def test_homepage_loads(self):
        self.driver.get(BASE_URL)
        self.assertIn("UWA Study Buddy", self.driver.title)

    # Tests for the signup page

    # Test the signup page loads and can submit the form
    def test_signup_page_loads(self):
        self.driver.get(f"{BASE_URL}/sign-up")
        self.assertIn("Sign Up", self.driver.title)

    # Fill the sign up form with arbitary values and submit the form

    def fill_signup_form(self, student_id="12345678", email="test@test.com", firstname="Dummy", lastname="User", username="dummyuser123", password="password123", course="Bachelor of Science", graduation="2025", birthday="1900-01-01"):
        self.driver.get(f"{BASE_URL}/sign-up")
        # Fill in the signup form
        self.driver.find_element(By.NAME, "student_id").send_keys(student_id)
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "firstname").send_keys(firstname)
        self.driver.find_element(By.NAME, "lastname").send_keys(lastname)
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "course").send_keys(course)
        self.driver.find_element(By.NAME, "graduation").send_keys(graduation)
        self.driver.find_element(By.NAME, "birthday").send_keys(birthday)

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Test that form validation works for student_id that is too short
    def test_short_student_id(self):
        self.fill_signup_form(student_id="1234")
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertIn("Invalid: Student ID must be 8 digits", error_message)

    # Test that form validation does not allow for duplicate primary keys
    def test_duplicate_student_id(self):
        random_id = str(random.randint(10000000, 99999999)) # Generates a random id that can be used to test duplicate student IDs
        self.fill_signup_form(student_id=random_id, username=f"first{random_id}")
        self.fill_signup_form(student_id=random_id, username=f"second{random_id}") # Duplicate student_id with different usetname
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertIn("Invalid: Student ID already has been registered.", error_message)

    # Test that sign up page succesfully submits a form and redirects to login page after successful sign up
    def test_signup_submits_and_redirects_to_login(self):
        random_id = str(random.randint(10000000, 99999999))
        self.fill_signup_form(student_id=random_id, username=f"user{random_id}") # Register a new random student ID with a unique username to test
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login-page"))
        self.assertIn("/login-page", self.driver.current_url)

    # Login
    def test_login_page_loads(self):
        self.driver.get(f"{BASE_URL}/login-page")
        self.assertIn("Login", self.driver.title)
    
