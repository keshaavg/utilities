# Filename: oauth_pkce_pcse.ipynb

import os
import base64
import hashlib
import secrets
import webbrowser
import requests
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# === Configuration ===
client_id = 'your-client-id'  # Replace this with your actual client ID
redirect_uri = 'http://localhost:8080/callback'
auth_url = 'https://your-auth-server.com/oauth/authorize'  # Replace with PCSE auth URL
token_url = 'https://your-auth-server.com/oauth/token'     # Replace with PCSE token URL
scopes = ['your_scope1', 'your_scope2']  # Replace with actual scopes

# === Step 1: Generate PKCE verifier and challenge ===
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(40)).rstrip(b'=').decode('utf-8')
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode('utf-8')

# === Step 2: Build the authorization URL ===
params = {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': ' '.join(scopes),
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256'
}
authorization_url = f"{auth_url}?{urlencode(params)}"

# === Step 3: Launch the browser for user login ===
print("Opening browser to complete login...")
webbrowser.open(authorization_url)

# === Step 4: Start temporary HTTP server to receive redirect ===
class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        self.server.auth_code = query.get('code', [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization complete. You may close this tab.")

httpd = HTTPServer(('localhost', 8080), OAuthCallbackHandler)
httpd.handle_request()
auth_code = httpd.auth_code

# === Step 5: Exchange authorization code for access token ===
token_data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'code_verifier': code_verifier
}

token_response = requests.post(token_url, data=token_data)
tokens = token_response.json()

# === Step 6: Show the access token (or store it)
access_token = tokens.get('access_token')
refresh_token = tokens.get('refresh_token')

print("Access Token:", access_token)
print("Refresh Token:", refresh_token)
