from flask import Flask, redirect, json, jsonify, Response, abort
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class TestRuns(db.Model):
  __tablename__ = 'test_runs'
  id = db.Column(db.String, primary_key = True)
  run_id = db.Column(db.Integer, db.ForeignKey('runs.id'), primary_key=True)
  test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), primary_key=True)
  status = db.Column(db.String)
  test = db.relationship('Test')

class Run(db.Model):
  __tablename__ = 'runs'
  id = db.Column(db.String, primary_key = True)
  passes = db.Column(db.Integer)
  skips = db.Column(db.Integer)
  fails = db.Column(db.Integer)
  tests = db.relationship('TestRuns')

  def __init__(self, id, passes, fails, skips):
    self.id = id
    self.passes = passes
    self.fails = fails
    self.skips = skips

  def success_percentage(self):
    if self.passes == 0:
      return 0

    total = self.passes + self.skips + self.fails
    percent =  (self.passes / float(total)) * 100
    truncated = int(percent)
    return truncated

  def serialize(self):
    return { 'id': self.id,
        'success_percentage': self.success_percentage(),
        'passes': self.passes,
        'fails': self.fails,
        'skips': self.skips }

class Test(db.Model):
  __tablename__ = 'tests'
  id = db.Column(db.String, primary_key = True)
  name = db.Column('test_id', db.String(256))

  def __init__(self, id, name):
    self.id = id
    self.name = name

  def serialize(self):
    return { 'id': self.id, 'name': self.name }

@app.route('/')
def index():
  return redirect('/runs', code=302)

@app.route('/runs')
def runs():
  runs = Run.query.all()
  data = [run.serialize() for run in runs]

  return jsonify(runs = data)

@app.route('/runs/<run_id>')
def run(run_id):
  run = Run.query.get(run_id)
  if run is None:
      abort(404)

  data = run.serialize()
  tests = [testrun.test.serialize() for testrun in run.tests]
  data['test_cases'] = tests

  return jsonify(data)

@app.route('/runs/<run_id>/test_cases')
def test_cases_by_run(run_id):
  run = Run.query.get(run_id)
  if run is None:
    abort(404)

  data = [testrun.test.serialize() for testrun in run.tests]

  return jsonify(test_cases = data)

if __name__ == '__main__':
  app.run(debug=True, host=os.getenv('HOST', 'localhost'))
