import json
import os
from datetime import datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload_video.py-oauth2.json')

if not os.path.exists(json_file_path):
    print(f'No OAuth token cache found at {json_file_path}; skipping refresh.')
    raise SystemExit(0)

with open(json_file_path, 'r') as file:
    credentials_data = json.load(file)

token_expiry = credentials_data.get('token_expiry')
if token_expiry:
    try:
        credentials_data['token_expiry'] = datetime.fromisoformat(
            token_expiry.replace('Z', '+00:00')
        )
    except ValueError:
        credentials_data['token_expiry'] = None
else:
    credentials_data['token_expiry'] = None

creds = Credentials(
    token=credentials_data['access_token'],
    refresh_token=credentials_data['refresh_token'],
    token_uri=credentials_data['token_uri'],
    client_id=credentials_data['client_id'],
    client_secret=credentials_data['client_secret'],
    scopes=credentials_data['scopes'],
    expiry=credentials_data.get('token_expiry')
)

if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    credentials_data['access_token'] = creds.token
    credentials_data['token_expiry'] = creds.expiry.isoformat() if creds.expiry else None

    with open(json_file_path, 'w') as file:
        json.dump(credentials_data, file, indent=4)
