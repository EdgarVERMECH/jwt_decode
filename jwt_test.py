import unittest
from unittest.mock import patch
from flask import Flask
from jose import jwt
import jwt_api

class TestYourFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = jwt_api.app
        self.client = self.app.test_client()

    def test_dummy_endpoint(self):
        response = self.client.get('/dummy')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"dummy":"ok"})

    @patch('jwt_api.verify_jwt_token')
    def test_verify_token_endpoint_with_no_token(self, mock_verify):
        response = self.client.post('/verify', json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"valid": False, "error": "Token manquant dans la requête."})

    @patch('jwt_api.verify_jwt_token')
    def test_verify_token_endpoint_with_invalid_token(self, mock_verify):
        mock_verify.return_value = None
        response = self.client.post('/verify', json={"token": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"valid": False, "error": "Le token JWT n'est pas valide."})

    @patch('jwt_api.verify_jwt_token')
    def test_verify_token_endpoint_with_valid_token(self, mock_verify):
        mock_payload = {"sub": "123", "name": "Test User"}
        mock_verify.return_value = mock_payload
        response = self.client.post('/verify', json={"token": "dummy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"valid": True, "message": "Le token JWT est valide.", "payload": mock_payload})

    def test_verify_token_endpoint_with_real_valid_token(self):
        payload = {"sub": "123", "name": "Test User"}
        public_key = "mspr_dolib@arr_edgar_edgar_lynda_pierre_alexandre"
        token = jwt.encode(payload, public_key, algorithm='HS256')

        response = self.client.post('/verify', json={"token": token})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"valid": True, "message": "Le token JWT est valide.", "payload": payload})

if __name__ == '__main__':
    unittest.main()
