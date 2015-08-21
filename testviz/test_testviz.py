import unittest
import testviz

class TestvizTestCase(unittest.TestCase):
  def setUp(self):
    self.app = testviz.app.test_client()
    testviz.init_db()

  def test_index(self):
    index = self.app.get('/')
    assert "build-item" in index.data

if __name__ == '__main__':
  unittest.main()
