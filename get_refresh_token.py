from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = '30364144312-4tsjc8mcml377fdl8gdh91nj5qh5lne0.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

flow = InstalledAppFlow.from_client_secrets_file(
    'creds.json', scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

auth_url, _ = flow.authorization_url(prompt='consent')

print(f'Please go to this URL to authorize the application: {auth_url}')
auth_code = input('Enter the authorization code: ')

flow.fetch_token(code=auth_code)
print(f'Refresh token: {flow.credentials.refresh_token}')
