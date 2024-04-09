import unittest
from unittest.mock import MagicMock

class TestCreatePlayer(unittest.TestCase):

    def setUp(self):
        self.request_mock = MagicMock()
        self.sql_functions_mock = MagicMock()

        import database
        self.module = database
        self.module.request = self.request_mock
        self.module.sql_functions = self.sql_functions_mock

    def test_create_player_valid_data(self):
        self.request_mock.get_json.return_value = {
            'username': 'random_user',
            'hashed_pass': 'random_pass',
            'email': 'random@email.com'
        }
        self.sql_functions_mock.select.return_value.first.return_value = None
        response = self.module.createPlayer()
        self.assertEqual(response, {'message': 'Added to database'})

    def test_create_player_sql_injection_attack(self):
        self.request_mock.get_json.return_value = {
            'username': 'random_userusername;DROP * connect4.PLAYERS',
            'hashed_pass': 'random_pass',
            'email': 'random@email.com'
        }
        self.sql_functions_mock.select.return_value.first.return_value = None
        response = self.module.createPlayer()
        self.assertEqual(response, {'message': 'Added to database'})

    def test_create_player_short_username(self):
        self.request_mock.get_json.return_value = {
            'username': 'srt',
            'hashed_pass': 'random_pass',
            'email': 'random@email.com'
        }
        response = self.module.createPlayer()
        self.assertEqual(response, {'message': 'Username must be at least 5 characters long'})

    def test_create_player_short_password(self):
        self.request_mock.get_json.return_value = {
            'username': 'random_user',
            'hashed_pass': 'short',
            'email': 'random@email.com'
        }
        response = self.module.createPlayer()
        self.assertEqual(response, {'message': 'Password must be at least 8 characters long'})

    def test_create_player_existing_user(self):
        self.request_mock.get_json.return_value = {
            'username': 'random_user',
            'hashed_pass': 'random_pass',
            'email': 'random@email.com'
        }
        response = self.module.createPlayer()
        self.assertEqual(response, {'message': 'Username already taken'})

    def test_create_player_special_characters_username(self):
        self.request_mock.get_json.return_value = {
            'username': 'user!@#',
            'hashed_pass': 'random_pass',
            'email': 'random@email.com'
        }
        response = self.module.createPlayer()
        self.assertEqual(response, {'message': 'Added to database'})

    def test_create_player_special_characters_password(self):
        self.request_mock.get_json.return_value = {
            'username': 'username',
            'hashed_pass': 'password!@#$%^&*()_+',
            'email': 'this@email.com'
        }
        response = self.module.createPlayer()
        self.assertEqual(response, {'message': 'Added to database'})

if __name__ == '__main__':
    unittest.main()