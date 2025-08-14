import requests
from django.conf import settings

def get_access_token():
    tenant_id = settings.TENANT_ID
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    scope = 'https://graph.microsoft.com/.default'
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    # This is the data block you're asking about:
    data = {
        'client_id': client_id,
        'scope': scope,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }

    # This is the call to request the token from Microsoft Identity Platform
    response = requests.post(token_url, data=data)
    response.raise_for_status()  # Raises an error if authentication fails

    # This returns the actual access token string from the JSON response
    return response.json()['access_token']
