from flask import Flask, render_template
import os # For the secret key
from routes.index import index_blueprint # For the index file
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'secret-key'

# Converts date from datetime (which is what it is stored as) to an actual string date
@app.template_filter('dateconverter')
def format_datetime(value):
    return datetime.fromtimestamp(value).strftime('%d %b %Y %I:%M %p')

# Register blueprint provided in index.py
app.register_blueprint(index_blueprint)

@app.route("/create-group")
def create_group():
    return render_template("createGroup.html")

@app.route("/my-groups")
def my_groups():
    return render_template("myGroups.html")

@app.route("/view-groups")
def view_groups():
    return render_template("viewGroups.html")

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)