import hashlib
import os

def generate_cnonce():
    return hashlib.md5(os.urandom(16)).hexdigest()

def generate_response_hash(method, path, challenge, username, password, nc, cnonce):
    ha1 = hashlib.md5(f"{username}:{challenge['realm']}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{path}".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{challenge['nonce']}:{nc}:{cnonce}:{challenge['qop']}:{ha2}".encode()).hexdigest()
    return response

def parse_challenge(header):
    prefix = 'Digest '
    challenge = header[len(prefix):]
    parts = challenge.split(',')
    params = {}
    for part in parts:
        key, value = part.strip().split('=')
        params[key] = value.strip('"')
    return params

def render_digest(params):
    parts = []
    for key, value in params.items():
        if key in ['nc', 'algorithm']:
            parts.append(f"{key}={value}")
        else:
            parts.append(f'{key}="{value}"')
    return 'Digest ' + ', '.join(parts)

class HttpDigest:
    def __init__(self, opts):
        if 'username' not in opts or 'password' not in opts:
            raise ValueError('Missing user and/or password!')
        self.username = opts['username']
        self.password = opts['password']
        self.nc = opts.get('nc', '00000001')
        self.cnonce = opts.get('cnonce', generate_cnonce())

    def handle_response(self, method, path, auth_headers):
        challenge = parse_challenge(auth_headers)
        request_params = {
            'username': self.username,
            'realm': challenge['realm'],
            'nonce': challenge['nonce'],
            'uri': path,
            'cnonce': self.cnonce,
            'nc': self.nc,
            'algorithm': 'MD5',
            'response': generate_response_hash(method, path, challenge, self.username, self.password, self.nc, self.cnonce),
            'qop': challenge['qop']
        }
        return render_digest(request_params)

    def inc_nonce(self):
        if self.nc == 'ffffffff':
            self.nc = '00000001'
        else:
            self.nc = f"{int(self.nc, 16) + 1:08x}"
        return self.nc

    def reset_nonces(self):
        self.nc = '00000001'
        self.cnonce = generate_cnonce()
        return True

def create_http_digest_client(opts):
    return HttpDigest(opts)