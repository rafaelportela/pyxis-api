import unittest
import pdb
import testviz
import json
from models import Run, Test, TestRuns

test_database_url = 'mysql://dashboard:password@192.168.33.42/sandbox_test'

app = testviz.app.test_client()
testviz.init_db(test_database_url)
from database import db_session

def clean_db():
  Run.query.delete()
  Test.query.delete()
  TestRuns.query.delete()
  db_session.commit()

class RunApiTestCase(unittest.TestCase):

  def setUp(self):
    clean_db()

    run = Run('1234', 80, 12, 8)
    testruns = TestRuns(status = "success")
    testruns.test = Test(123, 'nice test case')
    run.tests.append(testruns)
    db_session.add(run)
    db_session.commit()

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

  #def test_run_has_tests_as_sub_resources(self):
    #self.response = app.get('/runs/1234/tests')
    #self.run = json.loads(self.response.data)
    #self.assertEquals(len(self.run['tests']), 1)


class TestApiTestCase(unittest.TestCase):

  def setUp(self):
    clean_db()

    db_session.add(Test('13', 'nice test name'))
    db_session.commit()
    self.response = app.get('/tests')
    self.test = json.loads(self.response.data)[0]

  def test_get_tests(self):
    self.assertEquals(self.response.status_code, 200)

  def test_tests_have_name_attribute(self):
    self.assertEquals(self.test['name'], 'nice test name')



if __name__ == '__main__':
  unittest.main()
