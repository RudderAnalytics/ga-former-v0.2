import pandas as pd
from datetime import date, timedelta
import time

def transform(local_source_filename,local_out_filename):
	print ('[-] Starting data transformation...')
	transform_start_time = time.time()
		
	print ('[?] Importing raw data from csv file...')
	raw = pd.DataFrame.from_csv(local_source_filename, index_col=False)

	print ('[?] Rename uid column to ga:dimension2')
	raw.columns = ['ga:dimension2']

	print ('[?] Add new column ga:dimension60 with value = Former')
	raw['ga:dimension60'] = 'Former'

	print ('[?] Saving cleaned data to csv...')
	# export cleaned data to csv 	
	raw.to_csv(local_out_filename, index=False)
	
	print ('[x] Cleaned data saved to file: %s successfully.' % local_out_filename)
	print ('[x] Data transformed sucessfully in %s seconds' % (time.time() - transform_start_time))

if __name__ == '__main__':
	transform()