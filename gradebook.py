from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
#from flask_mysqldb import MySQL
#from datetime import datetime
#from flask_migrate import Migrate


app = Flask(__name__)
app.config["DEBUG"] = True

# Set up the database:
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ESIS668",
    password="python123",
    hostname="ESIS668.mysql.pythonanywhere-services.com",
    databasename="ESIS668$668gradebook",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



# Set up the login manager:
app.secret_key = "umbc2020"
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


# Object to hold all users
all_users = {
    "admin": User("admin", generate_password_hash("secret")),
    "bob": User("bob", generate_password_hash("less-secret")),
    "caroline": User("caroline", generate_password_hash("completely-secret")),
}

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

# Gradebook table
class Gradebook(db.Model):

    __tablename__ = "gradebook"

    s_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    major = db.Column(db.String(128))
    email = db.Column(db.String(128))
    a1 = db.Column(db.Integer)  #represents each assignment's grade
    a2 = db.Column(db.Integer)
    a3 = db.Column(db.Integer)
    a4 = db.Column(db.Integer)


# ROUTES

# Login page loading, functionality and error rendering
@app.route("/", methods=["GET", "POST"]) # Login is our homepage
def login():
    # Load the initial page
    if request.method == "GET":
        return render_template("login_page.html")

    # Variables for holding the login form and the User class
    form = request.form
    attempt = load_user(form["username"])

    # Validate user for login and redirect
    if attempt:     # attempt will be NULL and fail if not a valid user
        if User.check_password(attempt, form["password"]):
            login_user(attempt)
            return redirect(url_for("gradebook"))

    # If invalid user, reload with error message
    return render_template("login_page.html", error=True)

# Logout re-routing
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("/"))

# Gradebook page
@app.route("/gradebook", methods=["GET", "POST"])
#@login_required
def gradebook():
  if request.method == "GET":
     return render_template("gradebook.html", gradebk=Gradebook.query.all())

@app.route("/addstudent", methods=["GET", "POST"])
#@login_required
def addstudent():
    if request.method == "GET":
        return render_template("add_student.html")
    return render_template("add_student.html", error=True)

@app.route("/addstudentdata", methods=["POST"])
#@login_required
def addstudentdata():
    studentdata = Gradebook(fname=request.form["first_name"], lname=request.form["last_name"], s_id=request.form["student_id"], major=request.form["major_add"], email=request.form["email_address"])
    db.session.add(studentdata)
    db.session.commit()
    return redirect(url_for('addstudent'))

@app.route("/removestudent", methods=["GET", "POST"])
@login_required
def removestudent():
    if request.method == "GET":
        return render_template("remove_student.html")
    return render_template("remove_student.html", error=True)
