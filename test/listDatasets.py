from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from apiclient.discovery import build
import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage as CredentialStorage
from oauth2client.tools import run_flow as run_oauth2
from oauth2client import tools

import time
from datetime import date, timedelta
import os


def get_authenticated_service(scope):
    # define credential filepaths
    CLIENT_SECRETS_FILE = 'client_secrets.json'
    CREDENTIALS_FILE = 'credentials.json'
    
    print '[?] Authenticating...'
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=scope,
                                   message="")

    credential_storage = CredentialStorage(CREDENTIALS_FILE)
    credentials = credential_storage.get()
    if credentials is None or credentials.invalid:
        flags = tools.argparser.parse_args(args=[])
        credentials = run_oauth2(flow, credential_storage, flags)

    print '[?] Constructing Google Cloud Storage service...'
    http = credentials.authorize(httplib2.Http())

    service = build('analytics', 'v3', http=http)

    return service

def main():
    # Define the auth scopes to request.
    # RW_SCOPE = 'https://www.googleapis.com/auth/analytics'
    RO_SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'

    # Authenticate and construct service.
    service = get_authenticated_service(RO_SCOPE)

    try:
        uploads = service.management().uploads().list(
            accountId='3262475',  # www.fool.com
            webPropertyId='UA-3262475-1',  # http://www.fool.com
            customDataSourceId='gigvcD4-R-KQsEiDLSkZ-g'  # ad_cost_test
        ).execute()

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except HttpError, error:
        # Handle API errors.
        print ('There was an API error : %s : %s' %
            (error.resp.status, error.resp.reason))

    for upload in uploads.get('items', []):
        print 'Upload Id             = %s' % upload.get('id')
        print 'Upload Kind           = %s' % upload.get('kind')
        print 'Account Id            = %s' % upload.get('accountId')
        print 'Custom Data Source Id = %s' % upload.get('customDataSourceId')
        print 'Upload Status         = %s\n' % upload.get('status')

if __name__ == '__main__':
  main()