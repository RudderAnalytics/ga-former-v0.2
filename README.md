# The Motley Fool - Google Analytics Custom Data Import - Formers

## Scope 

1. Extract data from s3 bucket 
2. Transform data 
3. Upload data to GA via Management API
4. Delete old files from GA 
4. Log in Slack channel, monitor errors via Sentry

## Executive Summary 

The Motley Fool would like to make a customer's status (former) available in Google Analytics. The customer status data resides in The Motley Fool's data warehouse and is exported to a csv file in an Amazon S3 Bucket containing a list of all user id's who are former customers. This data then needs to be exported, transformed then uploaded to GA via the GA Management API.

## Details 

### Data Source

Amazon s3 Bucket:

- Name: `ad-costs`
- File Name: `formers.csv`
- Schema: 
    - `uid` - INTEGER
    - `isFormer` - STRING

### Data Destination

Google Analytics: 

- Property Name: `http://www.fool.com` 
- Property ID: `UA-3262475-1` 
- Data Set Name: `isFomer` 
- Data Set Type: `Custom Data (Query-Time)` 
- Data Set ID: `2bquzYQ3RKCM6Jha4VtrCQ` 
- Data Set Schema: `ga:dimension2,ga:dimension60` 

### Automation

- Uploads - daily at 0330 EDT / 0730 UTC
- Deletes - weekly at 0900 EDT / 1300 UTC

`$ sudo crontab -l`: 

```sh
### formers - US GA Property
#### Execute Import
30 7 * * * cd /ga/formers-us; python run.py
#### Weekly Cleanup
0 13 * * 5 cd /ga/formers-us, python cleanupGa.py
```

### Hosting

Google Compute Engine VM:

- GCP Project ID: `tmf-ep-gap`
- GCP Compute Instance Name: `df-g-1`
- Directory: `/ga/formers-us/`

### Source Code

- [run.py](https://github.com/justinjm/tmf-ga-formers-us/blob/master/run.py) - Executes the 4 scripts below in succession 
- [collect.py](https://github.com/justinjm/tmf-ga-formers-us/blob/master/collect.py) - Downloads file "formers.csv" and saves as "src.csv"
- [transform.py](https://github.com/justinjm/tmf-ga-formers-us/blob/master/transform.py) - Imports data from "src.csv", prepares it for loading into GA and saves as "formers_YYYYMMDD.csv"
    + See full details of transformation rules here: [transform_rules.md](https://github.com/justinjm/tmf-ga-formers-us/blob/master/transform_rules.md) 
- [load.py](https://github.com/justinjm/tmf-ga-formers-us/blob/master/load.py) - Imports "formers_YYYYMMDD.csv" into GA via Management API
- [log.py](https://github.com/justinjm/tmf-ga-formers-us/blob/master/log.py) - Sends a message to shared Slack channel (`#logs-motleyfool-ep`) for logging purposes
- [cleanupGa.py](https://github.com/justinjm/tmf-ga-formers-us/blob/master/cleanupGa.py) deletes old, redundant files from GA 

### Logging

Slack: 

- Owner: Empirical Path
- Channel: `#logs-motleyfool-ep`
- API Key: Please send email to Justin Marciszewski [justin@empiricalpath.com](mailto:justin@empiricalpath.com) to request.