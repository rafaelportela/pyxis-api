import unittest
import pdb
import testviz

test_database_url = 'mysql://dashboard:password@192.168.33.42/sandbox'

class RunsApi(unittest.TestCase):
  def setUp(self):
    self.app = testviz.app.test_client()
    testviz.init_db(test_database_url)

  def test_get_runs(self):
    response = self.app.get('/runs')
    self.assertEquals(response.status_code, 200)

if __name__ == '__main__':
  unittest.main()
