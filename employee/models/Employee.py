import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .employee import app
from flask_login import UserMixin

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "employee.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    department = db.Column(db.String(50), unique=False, nullable=False)
    date_of_joining = db.Column(db.String(50), unique=False, nullable=False)