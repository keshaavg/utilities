import os
import base64
import hashlib
import secrets
import webbrowser
import requests
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# Generate PKCE values
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(40)).rstrip(b'=').decode('utf-8')
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode('utf-8')

# Authorization URL
params = {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': ' '.join(scopes),
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256'
}
authorization_url = f"{auth_url}?{urlencode(params)}"
print("Authorization URL:", authorization_url)
webbrowser.open_new_tab(authorization_url)

# Local server to capture code
class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/auth/callback':
            query = parse_qs(parsed.query)
            self.server.auth_code = query.get('code', [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization complete. You may close this tab.")
        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer(('localhost', 8080), OAuthCallbackHandler)
httpd.handle_request()
auth_code = httpd.auth_code

# Exchange code for tokens
token_data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'code_verifier': code_verifier
}
tokens = requests.post(token_url, data=token_data).json()
access_token = tokens.get('access_token')
refresh_token = tokens.get('refresh_token')

print("Access Token:", access_token)
print("Refresh Token:", refresh_token)
