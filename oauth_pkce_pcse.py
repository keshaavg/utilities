# Filename: oauth_pkce_https_callback.ipynb

import os
import base64
import hashlib
import secrets
import webbrowser
import requests
import ssl
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# === CONFIGURATION ===
client_id = 'your-client-id'  # Replace with actual client ID
redirect_uri = 'https://localhost:8080/auth/callback'
auth_url = 'https://your-auth-server.com/oauth/authorize'  # Replace with actual auth URL
token_url = 'https://your-auth-server.com/oauth/token'     # Replace with actual token URL
scopes = ['your_scope1', 'your_scope2']  # Replace with required scopes

# === Generate PKCE verifier + challenge ===
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(40)).rstrip(b'=').decode('utf-8')
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode('utf-8')

# === Build the authorization URL ===
params = {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': ' '.join(scopes),
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256'
}
authorization_url = f"{auth_url}?{urlencode(params)}"

# === Define the HTTPS callback handler ===
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

# === Launch the authorization in browser ===
print("Opening browser for login...")
webbrowser.open(authorization_url)

# === Start HTTPS server to capture callback ===
httpd = HTTPServer(('localhost', 8080), OAuthCallbackHandler)

# Load self-signed cert
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Waiting for redirect to https://localhost:8080/auth/callback...")
httpd.handle_request()
auth_code = httpd.auth_code

# === Exchange auth code for access token ===
token_data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'code_verifier': code_verifier
}

token_response = requests.post(token_url, data=token_data)
tokens = token_response.json()

# === Display the result ===
print("Access Token:", tokens.get('access_token'))
print("Refresh Token:", tokens.get('refresh_token'))
