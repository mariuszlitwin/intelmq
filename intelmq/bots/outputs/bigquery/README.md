IntelMQ to Google BigQuery
===================

More information on BigQuery:
-------------------
https://cloud.google.com/bigquery/
https://cloud.google.com/bigquery/bq-command-line-tool

Installation:
-------------------
1. Install bot dependencies
`pip install google-api-python-client httpdlib2`
or use predefined REQUIREMENTS file
`pip install -r intelmq/bots/outputs/bigquery/REQUIREMENTS`
2. Initialize your Google BigQuery dataset
`bq mk --schema intelmq/bots/outputs/bigquery/intelmq.schema -t [mydataset.newtable]`
