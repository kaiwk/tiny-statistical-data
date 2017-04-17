import unittest

from website import register_blueprint

app = register_blueprint()

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.test_app = app.test_client()

if __name__ == '__main__':
    unittest.main()
