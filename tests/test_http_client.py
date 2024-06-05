import unittest
from unittest.mock import patch, MagicMock
from nirmata_rpc_module.http_client import create_http_client

class TestHttpClient(unittest.TestCase):
    def setUp(self):
        self.opts = {
            'url': 'http://localhost',
            'username': 'testuser',
            'password': 'testpass'
        }
        self.client = create_http_client(self.opts)

    @patch('nirmata_rpc_module.http_client.requests.Session')
    def test_create_http_client(self, MockSession):
        mock_session = MockSession.return_value
        client = create_http_client(self.opts)
        self.assertIsInstance(client, MagicMock)

    @patch('nirmata_rpc_module.http_client.requests.Session.request')
    def test_request(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        response = self.client.request('GET', 'http://localhost/test')
        self.assertEqual(response.status_code, 200)

    @patch('nirmata_rpc_module.http_client.requests.Session.request')
    def test_request_with_digest(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.headers = {'www-authenticate': 'Digest realm="testrealm", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", qop="auth"'}
        mock_request.return_value = mock_response

        with patch.object(self.client, 'http_digest') as mock_http_digest:
            mock_http_digest.handle_response.return_value = 'Digest ...'
            response = self.client.request('GET', 'http://localhost/test')
            self.assertEqual(response.status_code, 401)

    def test_reset_nonces(self):
        with patch.object(self.client, 'http_digest') as mock_http_digest:
            self.client.reset_nonces()
            mock_http_digest.reset_nonces.assert_called_once()

if __name__ == '__main__':
    unittest.main()