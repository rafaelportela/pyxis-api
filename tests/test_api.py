import unittest
import pdb
import json
from app import app, db
from app.runs.models import TestRuns, Run, Test

app = app.test_client()

def clean_db():
  Run.query.delete()
  Test.query.delete()
  TestRuns.query.delete()
  db.session.commit()

class RunApiTestCase(unittest.TestCase):

  def setUp(self):
    clean_db()

    run = Run('1234', 80, 12, 8)
    testruns = TestRuns(status = "success")
    testruns.test = Test(123, 'nice test case')
    run.tests.append(testruns)
    db.session.add(run)
    db.session.commit()

  def test_get_runs_index(self):
    self.response = app.get('/runs')
    self.assertEquals(self.response.status_code, 200)

  def test_run_has_id(self):
    self.response = app.get('/runs/1234')
    self.run = json.loads(self.response.data)
    self.assertEquals(self.run['id'], '1234')

  def test_run_has_success_percentage(self):
    self.response = app.get('/runs/1234')
    self.run = json.loads(self.response.data)
    self.assertEquals(self.run['success_percentage'], 80)

  def test_runs_has_passes_attribute(self):
    self.response = app.get('/runs/1234')
    self.run = json.loads(self.response.data)
    self.assertEquals(self.run['passes'], 80)

  def test_run_has_fails_attribute(self):
    self.response = app.get('/runs/1234')
    self.run = json.loads(self.response.data)
    self.assertEquals(self.run['fails'], 12)

  def test_run_has_skips_attribute(self):
    self.response = app.get('/runs/1234')
    self.run = json.loads(self.response.data)
    self.assertEquals(self.run['skips'], 8)

  def test_returns_404_when_not_found(self):
    self.response = app.get('/runs/12343')
    self.assertEquals(self.response.status_code, 404)

  def test_run_has_collection_of_test_cases(self):
    response = app.get('/runs/1234')
    run = json.loads(response.data)
    self.assertEquals(len(run['test_cases']), 1)
    self.assertEquals(run['test_cases'][0]['name'], 'nice test case')
    self.assertEquals(run['test_cases'][0]['status'], 'success')

  def test_run_has_tests_as_sub_resources(self):
    response = app.get('/runs/1234/test_cases')
    test_cases = json.loads(response.data)
    self.assertEquals(len(test_cases), 1)
    self.assertEquals(test_cases['test_cases'][0]['name'], 'nice test case')
    self.assertEquals(test_cases['test_cases'][0]['status'], 'success')

if __name__ == '__main__':
  unittest.main()
