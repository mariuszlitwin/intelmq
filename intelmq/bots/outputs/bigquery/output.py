# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

import json

import httplib2
from oauth2client.client import GoogleCredentials
from apiclient import discovery

from intelmq.lib.bot import Bot

# Bot can be copied right to the installed IntelMQ:
#   /usr/local/lib/python2.7/dist-packages/intelmq-1.0.0.dev4-py2.7.egg/intelmq/bots/outputs/bigquery/output.py
# BigQuery parameters:
#   project_id
#   dataset
#   table
# Other parameters:
#   chunk_size - count of events in request
#   dump_file - dump directory in case of request failure

class BigQueryBot(Bot):

    def init(self):
        # get default credentials
        credentials = GoogleCredentials.get_application_default()
        # aquire access to bigquery
        if credentials.create_scoped_required():
            credentials = credentials.create_scoped(['https://www.googleapis.com/auth/bigquery'])
        http = httplib2.Http()
        credentials.authorize(http)

        self.eventlist = list()

        self.chunk_size = int(self.parameters.chunk_size)
        self.dump_file = self.parameters.dump_file
        self.bigquery = discovery.build('bigquery', 'v2', http=http)

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return
        
        # append new event to list
        self.eventlist.append({"json": self.sanitize(event.to_dict())})
        
        # if there is enough events in list
        if len(self.eventlist) >= self.chunk_size:
            # setup parameters
            project_id = self.parameters.project_id
            dataset = self.parameters.dataset
            table = self.parameters.table

            body = {"ignoreUnknownValues": False,
                    "kind": "bigquery#tableDataInsertAllRequest",
                    "rows": self.eventlist,
                    "skipInvalidRows": False}

            # sent request to BigQuery
            request = self.bigquery.tabledata().insertAll(projectId=project_id, 
                                                           datasetId=dataset,
                                                           tableId=table, 
                                                           body=body)
            response = request.execute(num_retries=3)
            
            if 'insertErrors' in response:
                # TODO: better error handling
                self.logger.error(response)
                with open(self.dump_file, 'a') as fh:
                    json.dump(self.eventlist, fh)
            self.eventlist = list()

        self.acknowledge_message()
        
    def sanitize(self, event):
        if 'destination' in event:
            if 'ip' in event['destination']:
                event['destination']['ip'] = str(event['destination']['ip'])
            if 'local_ip' in event['destination']:
                event['destination']['local_ip'] = str(event['destination']['local_ip'])
            if 'network' in event['destination']:
                event['destination']['network'] = str(event['destination']['network'])
        if 'source' in event:
            if 'ip' in event['source']:
                event['source']['ip'] = str(event['source']['ip'])
            if 'local_ip' in event['source']:
                event['source']['local_ip'] = str(event['source']['local_ip'])
            if 'network' in event['source']:
                event['source']['network'] = str(event['source']['network'])
        if 'malware' in event and \
           'hash' in event['malware']:
            if isinstance(event['malware']['hash'], basestring):
                event['malware']['hash'] = {'value': event['malware']['hash']}
        
        return event


if __name__ == "__main__":
    bot = BigQueryBot(sys.argv[1])
    bot.start()

