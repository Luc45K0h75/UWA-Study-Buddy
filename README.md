# Welcome to UWA Study Buddy
## What is UWA Study Buddy?
UWA Study Buddy is a website created as our project in the CITS3403 Agile Web Development Unit. The purpose of the website is to be a study group finder that allows users to search for, create and join different study groups around the university. 

## Team Members
| Member | Role |
| :---: | :--- |
| Lucas Koh | Created frontend and backend for the home page, view groups page (with join group functionality) and my groups page. Made the database and wrote the selenium tests. Coded `app.py` and `models.py`. |
| Syifa Rahma Tsabita | Created the frontend and backend for the add groups page and the add sessions page. Responsible for creating all of the CSRF tokens across the website. |
| Bhavya Chhikara | Created the frontend and backend for the login and signup pages. Responsible for all of the authentication, authorisation and current user logic on the website. Wrote the unit tests. |
| Hamish Haslam | Created the front end and back end of the view profile page and responsible for the design of the website. |

## Tech Stack

| **Category** | **Technology** |
| :---: | :---: |
| Frontend | HTML5, CSS, Bootstrap 5, Javascript |
| Backend | Flask, Python 3 |
| Database | SQLite3, SQLAlchemy, Flask-Migrate |
| Security | Flask-Login, Werkzeug |
| Testing | unittest, Selenium |

## How to install and run UWA Study Buddy
1. Clone this repository:
```bash
git clone https://github.com/Luc45K0h75/UWA-Study-Buddy
cd UWA-Study-Buddy
```
2. Initialise virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Mac/Linux
venv\Scripts\activate     # for Windows
```

3. Install all of the libraries for this website:
```bash
pip install -r requirements.txt
```

4. Setup the database
```bash
flask db upgrade
```

5. Run the application:
```bash
flask run --port 5001
```

Tha app will now be available at `http://127.0.0.1:5001`. After installation only steps 2 and 5 of the above process will be needed to rerun the app. 

## Running Tests
### Selenium Tests
* To run the Selenium tests, Google Chrome and a live server will be required.
* We would recommend using two terminal windows with the following commands:

First terminal (to run flask and disable CSRF so the tests run correctly)
```bash
TESTING=True flask run --port 5001
```

Second terminal
**Terminal 2 — Run the tests:**
```bash
python -m pytest tests/test_selenium.py -v
```

## Pages of the Website
1. **Home Page (/, /index)** - Welcome page containing buttons to other pages, the user's upcoming events and the 3 most recent groups that have been created.
2. **Login Page (/login-page)** - Allows user to login to their account.
3. **Signup Page (/sign-up)** - Allows the user to sign up for an account on the website.
4. **My Groups Page (/my-groups)** - Allows a logged in user to view a list of groups they have joined.
5. **View Groups Page (/view-groups)** - Allows a logged in user to view all the different groups stored on the website. The user can filter by unit, faculty and/or group type. The user also joins groups on this page.
6. **Create Groups Page (/create-groups)** - Allows the user to create a group, adds it to the database and adds the user who creates it to the group as an admin.
7. **Add Sessions Page (/add-session)** - Allows the user to add a session to groups that they are an administrator of.
8. **View Profile Page (/view-profile)** - Allows users to view their profile details.
* The navbar at the top of the website allows users to navigate between pages.

## Other Design Notes
* Part of the viewProfile page (availability and study style in profile details) is not yet completed and will be developed in the future.
* The notifications button feature is disabled as it will be developed in the future.

## User Stories
* I am basing my story points on a complexity range whereby:
    * 1-3pts: a relatively easy task
    * 4-7pts: a moderately difficult task
    * 8-10pts: a very difficult task

| **#** | **Backlog Item (User Story)** | **Story Point** |
|:---:|:---:|:---:|
| 1 | As a new student at UWA, I would like to be able to quickly find  study groups for my units so that I don't fall behind on my units as the semester progresses | 5 |
| 2 | As a student who did well in a unit at UWA, I would like to create a small study group so that students currently undertaking that unit can join and learn the content efficiently and effectively | 5 |
| 3 | As a student at UWA who has joined many study groups, I would like to be able to see every study group that I have joined so that I know what groups I am a part of. | 2 |
| 4 | As the creator of a study group, I would like to be able to add our sessions onto the website so that all of the members of the group know when they are occuring. | 3 |
| 5 | As a student enrolled in a lot of groups, I would like to be able to see my closest upcoming events so that I can add them to my calendar. | 2 |
| 6 | As a developer responsible for maintaining the website, I want to make sure that users who are not logged in cannot access particular parts of the website (such as viewing profiles or joining groups) in order to ensure the integrity and security of the website. | 3 |
| 7 | As an administrator of the website, I would like to ensure that a student cannot input invalid data when registering a profile for the website so that there are no data integrity issues. | 1 |
| 8 | As a student, I want to ensure that my password is stored securely, so that in the case that the database is breached, my account is protected | 1 |
| 9 | As a new student at UWA, I would like to be able to sign up and login to the website so that I can quickly find new study groups. | 7 |
| 10 | As a student looking for a study group for my exam, I would like to be able to filter by study group type and unit so that it is easier for me to find what I am look for | 5 |


