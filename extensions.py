# File to prevent circular imports. Imports the database tables to be used in other files without importing the entire app.py file (which would cause circular imports).
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()