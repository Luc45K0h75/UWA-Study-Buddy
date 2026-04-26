# This code simply imports our database so that we don't have to import it every time

# Imports
import sqlite3 # We are using sqlite3 for our project's database
import os  # Used to get the path to the database

def get_data():
    path = os.path.dirname(os.path.abspath(__file__)) # Gets the path to where the database is stored
    database = os.path.join(path, "StudyBuddy.db") # This then retrieves the file path based on the path we found befor   
    connection = sqlite3.connect(database) # Creatse a connection to the database
    connection.row_factory = sqlite3.Row # Converts the data so it can be accessed by columns not just index
    return connection 