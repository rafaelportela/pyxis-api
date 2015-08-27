from flask import Flask, redirect, json, jsonify, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')

CORS(app)

db = SQLAlchemy(app)

from app.runs import controllers
