import unittest
import testviz

test_database_url = 'mysql://dashboard:password@192.168.33.42/sandbox'

class TestvizTestCase(unittest.TestCase):
  def setUp(self):
    self.app = testviz.app.test_client()
    testviz.init_db(test_database_url)

  def test_index(self):
    index = self.app.get('/')
    assert "build-item" in index.data

if __name__ == '__main__':
  unittest.main()
