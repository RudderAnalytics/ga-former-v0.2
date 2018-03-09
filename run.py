import time
from raven import Client
import collect
import transform
import load
import log


service_start_time = time.time()
print '[-] Starting service...'

client = Client(
    'https://7b2de0c690604e5eb136326ecf3dceaf:fca2bf5f0ed943fb8274d403042d621e@sentry.io/130821')


def run():
    try:
        collect.collect(bucket_name='ad-costs',
                        bucket_filename='formers.csv', 
                        local_source_filename='src.csv')
    except:
        client.captureException()
    else:
        try:
            transform.transform(local_source_filename='src.csv',
                                local_out_filename='formers.csv')
        except:
            client.captureException()
        else:
            try:
                load.load(file='formers.csv',
                          account_id='3262475',
                          web_property_id='UA-3262475-1',
                          dataset_id='2bquzYQ3RKCM6Jha4VtrCQ',
                          dataset_name='isFormer',
                          log_file='log.csv')
            except:
                client.captureException()
            else:
                try:
                    log.log(slack_channel='#logs-motleyfool-ep',
                            slack_text='Successfully uploaded formers data to Google Analytics.',
                            property_name='http://www.fool.com',
                            property_id='UA-3262475-1',
                            dataset_name='isFormer',
                            dataset_type='Custom Data (Query-Time)',
                            dataset_id='2bquzYQ3RKCM6Jha4VtrCQ',
                            dataset_schema='ga:dimension2,ga:dimension60',
                            dataset_ui_link='http://d.pr/hAOHDr')
                except:
                    client.captureException()
                else:
                    print('[X] Service finished successfully in %s seconds' %
                          (time.time() - service_start_time))

run()
