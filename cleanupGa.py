from raven import Client
import pandas as pd

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

from slacker import Slacker

import log


client = Client(
    'https://7b2de0c690604e5eb136326ecf3dceaf:fca2bf5f0ed943fb8274d403042d621e@sentry.io/130821')

print '[-] Initializing cleanup of GA...'


def load_log_file(log_filename):
    # load log file from local disk
    lf = pd.DataFrame.from_csv(log_filename, index_col=False)
    
    lf.columns = ['filename',
                  'id',
                  'kind',
                  'accountId',
                  'customDataSourceId',
                  'timestamp']

    lf['timestamp'] = pd.to_datetime(lf['timestamp'])

    return lf


def get_authenticated_service(scope):
    # authenticate with GA via service account ??
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

    http = credentials.authorize(httplib2.Http())

    service = build('analytics', 'v3', http=http)

    return service


def get_data_files(account_Id, web_Property_Id, custom_Data_Source_Id):
    # get list of data files uploaded to GA
    # Define the auth scopes to request
    SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'

    # Authenticate and construct service.
    service = get_authenticated_service(SCOPE)

    try:
        uploads = service.management().uploads().list(
            accountId=account_Id,
            webPropertyId=web_Property_Id,
            customDataSourceId=custom_Data_Source_Id
        ).execute()

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except HttpError, error:
        # Handle API errors.
        print('There was an API error : %s : %s' %
              (error.resp.status, error.resp.reason))

    # save results to dataframe
    gaDataFiles = pd.DataFrame(uploads['items'])

    gaDataFiles['id'] = gaDataFiles['id'].astype(str)

    return gaDataFiles


def data_files_to_delete(lf, gaDataFiles):
    # create a list of files to delete
    fileToSave = lf.ix[lf['timestamp'].idxmax()]

    gaDataFilesToDelete = gaDataFiles[gaDataFiles.id != fileToSave['id']]

    customDataImportUids = gaDataFilesToDelete['id'].get_values().tolist()

    body = {"customDataImportUids": customDataImportUids}

    return body


def delete_data_files(account_Id, web_Property_Id, custom_Data_Source_Id, req_body):
    # delete data uploaded to GA
    # Define the auth scopes to request.
    SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'

    # Authenticate and construct service.
    service = get_authenticated_service(SCOPE)

    # This request deletes a list of uploads.
    try:
        deletes = service.management().uploads().deleteUploadData(
            accountId=account_Id,
            webPropertyId=web_Property_Id,
            customDataSourceId=custom_Data_Source_Id,
            body=req_body).execute()

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except HttpError, error:
        # Handle API errors.
        print('There was an API error : %s : %s' %
              (error.resp.status, error.resp.reason))
    else:
        print 'data deleted from GA successfully'


def main():
    # Set GA account and property and dataset parameters
    ACCOUNT_ID = '3262475'  # www.fool.com
    PROPERTY_ID = 'UA-3262475-1'  # http://www.fool.com
    CUSTOM_DATA_ID = '2bquzYQ3RKCM6Jha4VtrCQ'
    CUSTOM_DATA_NAME = 'isFormer'
    logFilename = 'log.csv'

    # load log file from local disk
    log_file = load_log_file(log_filename=logFilename)
    print '[?] Log File from Local Disk: '
    print(log_file)

    # get list of uploaded files from GA
    gaDataFiles = get_data_files(account_Id=ACCOUNT_ID, web_Property_Id=PROPERTY_ID,
                                 custom_Data_Source_Id=CUSTOM_DATA_ID)
    print '[?] Files Uploaded to GA: '
    print(gaDataFiles)

    # create body for API request
    dftdBody = data_files_to_delete(lf=log_file, gaDataFiles=gaDataFiles)

    # print body, aka - data to delete from GA
    print '[?] Files to DELETE From GA: '
    print(dftdBody)

    # delete it from GA
    delete_data_files(account_Id=ACCOUNT_ID, web_Property_Id=PROPERTY_ID,
                      custom_Data_Source_Id=CUSTOM_DATA_ID, req_body=dftdBody)

    # tell slack about it
    log.log(slack_channel='#logs-motleyfool-ep',
            slack_text='Successfully deleted old formers data from Google Analytics.',
            property_name='http://www.fool.com',
            property_id='UA-3262475-1',
            dataset_name='isFormer',
            dataset_type='Custom Data (Query-Time)',
            dataset_id='2bquzYQ3RKCM6Jha4VtrCQ',
            dataset_schema='ga:dimension2,ga:dimension60',
            dataset_ui_link='http://d.pr/hAOHDr')

    print '[X] cleanup of GA completed successfully.'


if __name__ == '__main__':
    main()
