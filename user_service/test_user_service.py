import unittest
from unittest.mock import patch
from flask import json
from user_service.app import app

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('user_service.db.get_db_connection')
    def test_user_creation(self, mock_db_conn):
        # Mock the database connection and cursor
        mock_cursor = mock_db_conn.return_value.cursor.return_value
        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = [1]  # Simulate user ID after insert

        response = self.app.post('/users', data=json.dumps({'username': 'testuser', 'email': 'test@email.com'}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created', response.data)

    @patch('user_service.db.get_db_connection')
    def test_user_retrieval(self, mock_db_conn):
        # Mock the database connection and cursor
        mock_cursor = mock_db_conn.return_value.cursor.return_value
        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = {'id': 1, 'username': 'testuser', 'email': 'test@email.com'}

        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

if __name__ == '__main__':
    unittest.main()
