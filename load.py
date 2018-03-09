from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage as CredentialStorage
from oauth2client.tools import run_flow as run_oauth2
from oauth2client import tools

import time
import datetime
from datetime import date, timedelta
import csv


print '[-] Initializing data loading...'
load_start_time = time.time()

# Set GA API Auth parameters
CLIENT_SECRETS_FILE = 'client_secrets.json'
CREDENTIALS_FILE = 'credentials.json'


def get_authenticated_service(scope):

	print ('[?] Authenticating...')
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


def load(file,account_id,web_property_id,dataset_id,dataset_name,log_file):
	try:
		service = get_authenticated_service(scope='https://www.googleapis.com/auth/analytics')

		media = MediaFileUpload(file, 
								mimetype='application/octet-stream',
								resumable=False)

		uploads = service.management().uploads().uploadData(accountId=account_id,
			webPropertyId=web_property_id,
			customDataSourceId=dataset_id,
			media_body=media).execute()

		print ('[?] Initiating upload of %s to dataset %s...' % (file, dataset_name))

	except TypeError, error:
		# Handle errors in constructing a query.
		print ('There was an error in constructing your query : %s' % error)

	except HttpError, error:
		# Handle API errors.
		print ('There was an API error : %s : %s' %(error.resp.status, error.resp.reason))

	print ('Upload Id = %s' % uploads.get('id'))
	print ('Upload Kind = %s' % uploads.get('kind'))
	print ('Account Id = %s' % uploads.get('accountId'))
	print ('Custom Data Source Id = %s' % uploads.get('customDataSourceId'))
	print ('Upload Status = %s\n' % uploads.get('status'))

	fields=[file,uploads.get('id'),uploads.get('kind'),
	uploads.get('accountId'),uploads.get('customDataSourceId'),
	datetime.datetime.now()]

	## write to csv
	with open(log_file, 'a') as f:
	    writer = csv.writer(f)
	    writer.writerow(fields)


if __name__ == '__main__':
	load()