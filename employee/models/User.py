import os
from flask import Flask
from flask_login import UserMixin
from .employee import app
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "employee.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)