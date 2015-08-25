import unittest
import pdb
import testviz
import json
from models import Run, Test

test_database_url = 'mysql://dashboard:password@192.168.33.42/sandbox_test'

app = testviz.app.test_client()
testviz.init_db(test_database_url)
from database import db_session

class RunApiTestCase(unittest.TestCase):

  def setUp(self):
    Run.query.delete()
    db_session.add(Run('1234', 80, 12, 8))
    db_session.commit()
    self.response = app.get('/runs')
    self.run = json.loads(self.response.data)[0]

  def test_get_runs(self):
    self.assertEquals(self.response.status_code, 200)

  def test_runs_have_id(self):
    self.assertEquals(self.run['id'], '1234')

  def test_runs_have_success_percentage(self):
    self.assertEquals(self.run['success_percentage'], 80)

  def test_runs_have_passes_attribute(self):
    self.assertEquals(self.run['passes'], 80)

  def test_runs_have_fails_attribute(self):
    self.assertEquals(self.run['fails'], 12)

  def test_runs_have_skips_attribute(self):
    self.assertEquals(self.run['skips'], 8)

class TestApiTestCase(unittest.TestCase):

  def setUp(self):
    Test.query.delete()
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
