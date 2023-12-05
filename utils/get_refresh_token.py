from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

flow = InstalledAppFlow.from_client_secrets_file(
    '../creds.json', scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

auth_url, _ = flow.authorization_url(prompt='consent')

print(f'Please go to this URL to authorize the application: {auth_url}')
auth_code = input('Enter the authorization code: ')

flow.fetch_token(code=auth_code)
print(f'Refresh token: {flow.credentials.refresh_token}')
