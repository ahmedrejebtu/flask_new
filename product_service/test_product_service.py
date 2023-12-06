import unittest
from unittest.mock import patch
from flask import json
from product_service.app import app

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('product_service.db.get_db_connection')
    def test_product_update(self, mock_db_conn):
        # Mock the database connection and cursor
        mock_cursor = mock_db_conn.return_value.cursor.return_value
        mock_cursor.execute.return_value = None
        mock_cursor.rowcount = 1  # Simulate one row updated

        response = self.app.put('/products/1', data=json.dumps({'name': 'New Product', 'price': 99.99}), 
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product updated', response.data)

    @patch('product_service.db.get_db_connection')
    def test_product_deletion(self, mock_db_conn):
        # Mock the database connection and cursor
        mock_cursor = mock_db_conn.return_value.cursor.return_value
        mock_cursor.execute.return_value = None
        mock_cursor.rowcount = 1  # Simulate one row deleted

        response = self.app.delete('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product deleted', response.data)

if __name__ == '__main__':
    unittest.main()
