import unittest
import pdb
import testviz
import json
from models import Run

test_database_url = 'mysql://dashboard:password@192.168.33.42/sandbox_test'

class RunsApi(unittest.TestCase):

  def setUp(self):
    self.app = testviz.app.test_client()
    testviz.init_db(test_database_url)
    from database import db_session
    Run.query.delete()
    db_session.add(Run('1234', 80, 12, 8))
    db_session.commit()
    self.response = self.app.get('/runs')
    self.run = json.loads(self.response.data)[0]

  def test_get_runs(self):
    self.assertEquals(self.response.status_code, 200)

  def test_runs_have_id(self):
    self.assertEquals(self.run['id'], '1234')

  def test_runs_have_success_percentage(self):
    self.assertEquals(self.run['success_percentage'], 80)

if __name__ == '__main__':
  unittest.main()
