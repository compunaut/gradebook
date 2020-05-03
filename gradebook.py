from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
from flask_migrate import Migrate

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
migrate = Migrate(app, db)

mycursor = db.cursor()

# Set up the login manager:
app.secret_key = "umbc2020"
login_manager = LoginManager()
login_manager.init_app(app)


# DATABASE TABLES:

# User table
class User(UserMixin, db.Model):

    __tablename__ = "users"

    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return self.username

# Gradebook table
class Gradebook(UserMixin, db.Model):

    _tablename_ = "gradebook"

    s_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    major = db.Column(db.String(128))
    email = db.Column(db.String(128))
    a1 = db.Column(db.Integer)  #represents each assignment's grade
    a2 = db.Column(db.Integer)
    a3 = db.Column(db.Integer)
    a4 = db.Column(db.Integer)

'''
# Student table
class Student(UserMixin, db.Model):

    _tablename_ = "students"

    s_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    major = db.Column(db.String(128))
    email = db.Column(db.String(128))

    def add_student():
        return #????? - make a new record
    def remove_student(self):
        return #????? - delete a record

# Course table
class Course(UserMixin, db.Model):

    _tablename_ = "course"

    c_id = db.Column(db.Integer, primary_key=True)
    c_title = db.Column(db.String(128))

    def add_course():
        return #????? - make a new record
    def remove_course(self):
        return #????? - delete a record

#Assignment table
class Assignment(UserMixin, db.Model):

    _tablename_ = "assignment"

    a_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, foreign_key=True)
    #c_id = db.ForeignKey('course.c_id', on_delete=db.CASCADE)

    def add_assignment():
        return #????? - make a new record
    def remove_assignment(self):
        return #????? - delete a record

"""
#Gradebook Table
class Gradebook(UserMixin, db.Model):

    _tablename_ = "gradebook"

    c_id = db.Column(db.Integer, foreign_key=True)
    s_id = db.Column(db.Integer, foreign_key=True)
    a_id = db.Column(db.Integer, foreign_key=True)
    grade = db.Column(db.Integer)

    def add_grade():
        return #????? - make a new record
    def remove_grade(self):
        return #????? - delete a record
    def change_grade(self):
        return #????? - edit a record
"""
'''

# Handle login function, calling user information from id
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()



# ROUTES

# Login Page - login is our homepage
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html")

# Logout re-routing
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))

# Course selection page
@app.route('/course/')
def course_roster():
    return render_template("course_roster.html")

# Gradebook page
@app.route('/gradebook/', methods=["GET", "POST"])
def gradebook():
  if request.method == "GET":
       mycursor.execute('SELECT * FROM Gradebook')
       data = mycursor.fetchall()
       return render_template('gradebook.html', data = data)

# Student info page
@app.route('/student/') # may not need a 'student' page if gradebook is detailed
def load_student(s_id):
    return render_template("student_info.html")

