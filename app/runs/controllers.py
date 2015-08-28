from flask import redirect, json, jsonify, Response, abort
from app import app
from app.runs.models import Run

@app.route('/')
def index():
  return redirect('/runs', code=302)

@app.route('/runs')
def runs():
  runs = Run.query.limit(10).all()
  data = [run.serialize() for run in runs]

  return jsonify(runs = data)

@app.route('/runs/<run_id>')
def run(run_id):
  run = Run.query.get(run_id)
  if run is None:
      abort(404)

  data = run.serialize()

  data['test_cases'] = tests_with_status(run.testruns)

  return jsonify(data)

@app.route('/runs/<run_id>/test_cases')
def test_cases_by_run(run_id):
  run = Run.query.get(run_id)
  if run is None:
    abort(404)

  return jsonify(test_cases = tests_with_status(run.testruns))

def tests_with_status(test_cases_collection):
  tests = []
  for testrun in test_cases_collection:
      single_test_case = testrun.test.serialize()
      single_test_case['status'] = testrun.status
      tests.append(single_test_case)

  return tests
