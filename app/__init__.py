from flask import Flask, redirect, json, jsonify, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from app.runs import controllers
