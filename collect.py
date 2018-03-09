import boto.s3.connection
import time


def collect(bucket_name,bucket_filename,local_source_filename):
	collect_start_time = time.time()
	print ('[-] Starting data collection...')
	
	print ('[-] Connecting to AWS...')
	conn = boto.s3.connection.S3Connection('AKIAJJELSXG7OSMVDQMQ', 'wjgYKopdp8Kt3ZKH5LqG3/vz43rfb5vtOSds/BWU')

	buck = conn.get_bucket(bucket_name)
	key = buck.get_key(bucket_filename)
	key.get_contents_to_filename(local_source_filename)
	
	print('[x] Collection completed successfully in %s seconds' % (time.time() - collect_start_time))

if __name__ == '__main__':
	collect()