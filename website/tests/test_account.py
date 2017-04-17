import unittest

from website import register_blueprint

app = register_blueprint()

class AccountTestCase(unittest.TestCase):

    def setUp(self):
        self.test_app = app.test_client()

    def tearDown(self):
        pass


    def login(self, username, password):
        return self.test_app.post('/account/login/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        rv = self.login('kermit', '12345')
        assert b'Logout' in rv.data

    def logout(self):
        return self.test_app.get('/account/logout/', follow_redirects=True)

    def test_logout(self):
        rv = self.logout()
        assert b'Login' in rv.data


if __name__ == '__main__':
    unittest.main()
