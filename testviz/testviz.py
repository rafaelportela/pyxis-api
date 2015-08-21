from flask import Flask
from flask import render_template
from flask import json
from flask import Response
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

from database import init_db
from database import db_session
from models import Run

init_db()

@app.route('/')
def index():
  runs = Run.query.limit(5).all()
  return render_template('index.html', runs = runs)

@app.route('/runs')
def runs():
  runs = Run.query.limit(5).all()
  data = [run.serialize() for run in runs]

  return Response(json.dumps(data), status=200, mimetype="application/json")

if __name__ == '__main__':
  app.run(debug=True, host=os.getenv('HOST', 'localhost'))
