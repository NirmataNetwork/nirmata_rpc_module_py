import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .httpDigest import create_http_digest_client

class HttpClient:
    def __init__(self, opts):
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1)))
        self.session.mount('https://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1)))
        self.session.headers.update({'Content-Type': 'application/json'})
        self.digest_handler_enabled = False
        self._retry = False

        if 'username' in opts and 'password' in opts:
            self.http_digest = create_http_digest_client(opts)
            self.www_auth = ''
            self.digest_handler_enabled = True

    def request(self, method, url, **kwargs):
        if self.digest_handler_enabled:
            self.session.headers.update({
                'Authorization': self.http_digest.handle_response(method, url, self.www_auth)
            })
            self.http_digest.inc_nonce()

        response = self.session.request(method, url, **kwargs)

        if self.digest_handler_enabled and response.status_code == 401 and not self._retry:
            self.www_auth = response.headers.get('www-authenticate', '')
            self.session.headers.update({
                'Authorization': self.http_digest.handle_response(method, url, self.www_auth)
            })
            self.http_digest.inc_nonce()
            self._retry = True
            return self.request(method, url, **kwargs)

        self._retry = False
        response.raise_for_status()
        return response

    def reset_nonces(self):
        return self.http_digest.reset_nonces()

def create_http_client(opts):
    return HttpClient(opts)