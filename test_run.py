import time
# from raven import Client
import collect
import transform
import load
import log


service_start_time = time.time()
print '[-] Starting service...'

# client = Client(
#     'URL')


def run():
    try:
        collect.collect(bucket_name='ad-costs', bucket_filename='formers.csv',
                        local_source_filename='src_test.csv')
    except Exception as e:
        print 'Collect failed !'
        print e
    else:
        try:
            transform.transform(local_source_filename='src_test.csv',
                                local_out_filename='formers_test.csv')
        except Exception as e:
            print 'Tranform failed!'
            print e
        else:
            try:
                load.load(file='formers_test.csv',
                          account_id='3262475',
                          web_property_id='UA-3262475-1',
                          dataset_id='peWbWL_OQEWmDPPaAUVkLw',
                          dataset_name='z_isFormer_test',
                          log_file='log_test.csv')
            except Exception as e:
                print 'Load failed!'
                print e
            else:
                try:
                    log.log(slack_channel='#test',
                            slack_text='Successfully uploaded formers to Google Analytics.',
                            property_name='http://www.fool.com',
                            property_id='UA-3262475-1',
                            dataset_name='z_isFormer_test',
                            dataset_type='Custom Data (Query-Time)',
                            dataset_id='peWbWL_OQEWmDPPaAUVkLw',
                            dataset_schema='ga:dimension2,ga:dimension60',
                            dataset_ui_link='http://d.pr/hAOHDr')
                except Exception as e:
                    print 'Log failed!'
                    print e
                else:
                    print('[X] Service finished successfully in %s seconds'
                          % (time.time() - service_start_time))
run()
