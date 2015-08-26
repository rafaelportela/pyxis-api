from flask import redirect, json, jsonify, Response, abort
from app import app
from app.runs.models import Run

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
