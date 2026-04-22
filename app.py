from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

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