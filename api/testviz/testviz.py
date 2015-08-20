from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

from database import init_db
from database import db_session
from models import Run

init_db()

@app.route('/')
def index():
  runs = Run.query.all()
  return render_template('index.html', runs = runs)

app.run(debug=True)
