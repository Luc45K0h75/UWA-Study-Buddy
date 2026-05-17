# Selenium tests for the functionality of signup and login pages.
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Base URL for the Flask app
BASE_URL = 'http://127.0.0.1:5001'

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

    def fill_signup_form(self, student_id="12345678", email=None, firstname="Dummy", lastname="User", username="dummyuser123", password="password123", course="Bachelor of Science", graduation="2029", birthday="2000-01-01"):
        # Generate a random email if not provided 
        if email is None:
            email = f"test{random.randint(1, 99999)}@gmail.com"
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

        time.sleep(1) # Allow the page to fully render and process the input before submitting the form
        
        # Submit the form 
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].click();", button)

    # Test that form validation works for student_id that is too short
    def test_short_student_id(self):
        self.fill_signup_form(student_id="1234")
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertIn("Invalid: Student ID must be 8 digits", error_message)

    # Test that form validation does not allow for duplicate primary keys
    def test_duplicate_student_id(self):
        random_id = str(random.randint(10000000, 99999999)) # Generates a random id that can be used to test duplicate student IDs
        email1 = f"test{random.randint(1, 99999)}@gmail.com" # Generates a random email for the first signup
        email2 = f"test{random.randint(100000, 199999)}@gmail.com" # Generates a random email for the second signup
        self.fill_signup_form(student_id=random_id, username=f"first{random_id}", email=email1) # First signup with the random student ID and first email
        self.fill_signup_form(student_id=random_id, username=f"second{random_id}", email=email2) # Duplicate student_id with different username and email
        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertIn("Student ID already has been registered.", error_message)

    # Test that sign up page succesfully submits a form and redirects to login page after successful sign up
    def test_signup_submits_and_redirects_to_login(self):
        random_id = str(random.randint(10000000, 99999999))
        self.fill_signup_form(student_id=random_id, username=f"user{random_id}") # Register a new random student ID with a unique username to test
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login-page"))
        self.assertIn("/login-page", self.driver.current_url)
        print(f"Current URL after submit: {self.driver.current_url}")
        print(f"Page source: {self.driver.page_source[:500]}")

    # Login Page Tests

    # Test login page loads correctly
    def test_login_page_loads(self):
        self.driver.get(f"{BASE_URL}/login-page")
        self.assertIn("Login", self.driver.title)

    # Test that login works with correct credentials and redirects to profile page
    def test_login_with_correct_credentials(self):
        # Test depends on signup working correctly
        # Create a new test user
        random_id = str(random.randint(10000000, 99999999))
        self.fill_signup_form(student_id=random_id, username=f"testuser{random_id}")

        # Login with the created user
        self.driver.get(f"{BASE_URL}/login-page")

        # Login with the created user
        self.driver.find_element(By.NAME, "username").send_keys(f"testuser{random_id}")
        self.driver.find_element(By.NAME, "password").send_keys("password123")

        time.sleep(1) # Allow the page to fully render and process the input before submitting the form

        # Submit the login form
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].click();", button)

        # Redirects to profile page after login
        WebDriverWait(self.driver, 10).until(EC.url_contains("/view-profile"))
        self.assertIn("/view-profile", self.driver.current_url)

    # Test that login does not work with incorrect credentials
    def test_login_with_incorrect_credentials(self):
        self.driver.get(f"{BASE_URL}/login-page")

        # Generate an unregistered username and subsequent unregistered password
        self.driver.find_element(By.NAME, "username").send_keys("wronguser") 
        self.driver.find_element(By.NAME, "password").send_keys("wrongpassword")

        time.sleep(1) # Allow the page to fully render and process the input before submitting the form

        # Submit the login form
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].click();", button)

        error_message = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertIn("Invalid Username or Password, please try again", error_message)


    # Test unauthenticated redirect from view profile page if not logged in
    def test_unauthenticated_redirect_to_login(self):
        # Attempt to access the profile page without logging in
        self.driver.get(f"{BASE_URL}/view-profile")

        # Should be redirected to login page
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login-page"))
        self.assertIn("/login-page", self.driver.current_url)

    # My Groups Tests

    # Test that /my-groups redirects to login if the user is not logged in
    def test_my_groups_unauthenticated_redirect(self):
        self.driver.get(f"{BASE_URL}/my-groups")
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login-page"))
        self.assertIn("/login-page", self.driver.current_url)

    # Test that the My Groups page loads and the Sessions column is present after logging in
    def test_my_groups_sessions_column_exists(self):
        # Create and log in a new user
        random_id = str(random.randint(10000000, 99999999))
        self.fill_signup_form(student_id=random_id, username=f"testuser{random_id}")
        self.driver.get(f"{BASE_URL}/login-page")
        self.driver.find_element(By.NAME, "username").send_keys(f"testuser{random_id}")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        time.sleep(1)
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].click();", button)
        WebDriverWait(self.driver, 10).until(EC.url_contains("/view-profile"))

        # Navigate to My Groups and check the Sessions column header is present
        self.driver.get(f"{BASE_URL}/my-groups")
        WebDriverWait(self.driver, 10).until(EC.url_contains("/my-groups"))
        headers = self.driver.find_elements(By.TAG_NAME, "th")
        header_texts = [h.text for h in headers]
        self.assertIn("Sessions", header_texts)