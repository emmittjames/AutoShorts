#!/usr/bin/python

import json
import os
import random
import time
from datetime import datetime, timedelta

import httplib2
import requests
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.tools import argparser


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "upload_video.py-oauth2.json")

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

%s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def load_client_config():
    try:
        with open(CLIENT_SECRETS_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise SystemExit(MISSING_CLIENT_SECRETS_MESSAGE)

    client_info = data.get('installed')
    if not client_info:
        raise SystemExit("client_secrets.json must contain an installed OAuth client config for device-code auth.")

    return client_info['client_id'], client_info['client_secret']


def save_token_file(token_data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=4)


def build_credentials_from_data(data):
    token_expiry = data.get('token_expiry')
    expiry = None
    if token_expiry:
        try:
            token_expiry = token_expiry.replace('Z', '+00:00')
            expiry = datetime.fromisoformat(token_expiry)
        except Exception:
            expiry = None

    return Credentials(
        token=data.get('access_token'),
        refresh_token=data.get('refresh_token'),
        token_uri=data.get('token_uri'),
        client_id=data.get('client_id'),
        client_secret=data.get('client_secret'),
        scopes=data.get('scopes'),
        expiry=expiry,
    )


def get_device_code_credentials():
    client_id, client_secret = load_client_config()
    response = requests.post(
        'https://oauth2.googleapis.com/device/code',
        data={'client_id': client_id, 'scope': YOUTUBE_UPLOAD_SCOPE},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    verification_url = payload.get('verification_url', 'https://www.google.com/device')
    user_code = payload.get('user_code')
    device_code = payload.get('device_code')
    interval = int(payload.get('interval', 5))
    expires_in = int(payload.get('expires_in', 1800))

    print("Open this URL on another device:")
    print(verification_url)
    print(f"Enter this code: {user_code}")

    deadline = time.time() + expires_in
    poll_interval = interval

    while time.time() < deadline:
        time.sleep(poll_interval)
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'device_code': device_code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            },
            timeout=30,
        )
        token_payload = token_response.json()

        error = token_payload.get('error')
        if 'access_token' in token_payload:
            token_payload['token_uri'] = 'https://oauth2.googleapis.com/token'
            token_payload['client_id'] = client_id
            token_payload['client_secret'] = client_secret
            token_payload['scopes'] = [YOUTUBE_UPLOAD_SCOPE]
            token_payload['token_expiry'] = (
                datetime.now() + timedelta(seconds=int(token_payload.get('expires_in', 3600)))
            ).isoformat()
            save_token_file(token_payload)
            return build_credentials_from_data(token_payload)

        if error == 'authorization_pending':
            continue
        if error == 'slow_down':
            poll_interval += 5
            continue
        if error == 'access_denied':
            raise SystemExit('The user denied access to the Google account.')

        raise SystemExit(f"Google device auth failed: {token_payload}")

    raise SystemExit('Google device auth timed out before the user completed verification.')


def get_authenticated_service(args):
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as f:
                data = json.load(f)
            creds = build_credentials_from_data(data)

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                data['access_token'] = creds.token
                data['token_expiry'] = creds.expiry.isoformat() if creds.expiry else None
                save_token_file(data)
                return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=creds)

            if creds.valid:
                return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=creds)
        except (RefreshError, ValueError, TypeError, OSError, json.JSONDecodeError):
            pass

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=get_device_code_credentials())


def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(",")

    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." %
                        response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                    e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


if __name__ == '__main__':
    argparser.add_argument("--file", required=True,
                        help="Video file to upload")
    argparser.add_argument("--title", help="Video title", default="Test Title")
    argparser.add_argument("--description", help="Video description",
                        default="Test Description")
    argparser.add_argument("--category", default="22",
                        help="Numeric video category. " +
                        "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    argparser.add_argument("--keywords", help="Video keywords, comma separated",
                        default="")
    argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                        default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
    args = argparser.parse_args()

    if not os.path.exists(args.file):
        exit("Please specify a valid file using the --file= parameter.")

    youtube = get_authenticated_service(args)
    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))