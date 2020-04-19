from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config["DEBUG"] = True


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ESIS668",
    password="Kon@bik",
    hostname="ESIS668.mysql.pythonanywhere-services.com",
    databasename="ESIS668$668gradebook",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Route for handling the login page logic
@app.route('/sign_in', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'professor1' or request.form['password'] != 'umbc123':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('class_selection.html'))
    return render_template('sign_in.html', error=error)

# Route for returing a given class' roster
@app.route('/class')
def route():
    return render_template('flaskroute.html')

