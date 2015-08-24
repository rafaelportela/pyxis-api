from flask import Flask
from flask import render_template
from flask import json
from flask import Response
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

from database import init_db
from models import Run

database_url = os.getenv('DATABASE_URL', 'mysql://dashboard:password@192.168.33.42/sandbox')
init_db(database_url)

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
