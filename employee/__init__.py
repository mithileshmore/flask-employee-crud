import os
from flask import Flask, Blueprint, url_for, flash, session
from flask import render_template
from flask import request, redirect

from flask_bootstrap import Bootstrap
from flask_login import UserMixin
# from models import User, Employee
from employee.models import User, Employee

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, LoginManager

auth = Blueprint('auth', __name__)

app = Flask(__name__)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

def __repr__(self):
    Employee.format(self.employee_name)
    Employee.format(self.last_name)
    Employee.format(self.department)
    Employee.format(self.date_of_joining)

@app.route("/")
def welcome():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    return render_template("welcomePage.html")

@app.route("/home")
def home():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    return render_template("homePage.html")

@login_manager.user_loader
def load_user(user_id):
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.form:
        username = request.form.get('userName')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()
        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, password): 
            print('Please check your login details and try again.')
            # if user doesn't exist or password is wrong, reload the page
            return render_template("loginPage.html")
            return redirect("login")
        print(user)
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        session['logged_in'] = True
        return redirect(url_for("home"))
    else:
        return render_template("loginPage.html")

@app.route('/signup', methods=["POST", "GET"])
def signup():
    # if not session.get('logged_in'):
    #     return redirect(url_for("login"))
    if request.form:
        username = request.form.get('userName')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first() # if this returns a user, then the username already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again  
            print('username address already exists')
            return redirect(url_for("signup"))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("signupPage.html")

@app.route('/logout')
# @login_required   
def logout():
    logout_user()
    return redirect(url_for("login"))
    # return render_template("loginPage.html")

@app.route("/add", methods=["GET","POST"])
def add():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    if request.form:
        employee = Employee(employee_name = request.form.get("employeeName"), last_name = request.form.get("lastName"), department = request.form.get("department"), date_of_joining = request.form.get("dateOfJoining"))
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("addPage.html")

@app.route("/view")
def view():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    employees = Employee.query.all()
    return render_template("viewPage.html", employees=employees)

@app.route("/delete", methods=["POST", "GET"])
def delete():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    if request.form:
        employee = Employee.query.filter_by(id=request.form.get("id")).first()
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for("home"))
    employees = Employee.query.all()
    return render_template("deletePage.html", employees=employees)

@app.route("/update", methods=["POST", "GET"])
def update():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    if request.form:
        employee = Employee.query.filter_by(id=request.form.get("id")).first()
        employeeName = request.form.get("employeeName")
        lastName = request.form.get("lastName")
        department = request.form.get("department")
        employee.employee_name = employeeName
        employee.last_name = lastName
        employee.department = department
        db.session.commit()
    employees = Employee.query.all()
    return render_template("updatePage.html", employees=employees)
