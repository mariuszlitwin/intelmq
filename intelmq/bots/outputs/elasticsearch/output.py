# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

import json
import elasticsearch

from intelmq.lib.bot import Bot


class ElasticSearch(Bot):
    def init(self):
        self.es = elasticsearch.Elasticsearch([
            {'host': self.parameters.host, 'port': self.parameters.port}
        ])

    def process(self):
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return
        
        # dirty hack to avoid harmonization check
        event_dict = event.to_dict()
        
        # event field tweaking (for geolocation and other shit...)
        for key in ['source', 'destination']:
            if key in event_dict: 
                if 'geolocation' in event_dict[key]:
                    if 'latitude' in event_dict[key]['geolocation'] and \
                       'longitude' in event_dict[key]['geolocation']:
                            event_dict[key]['geolocation']['location'] = '{latitude}, {longitude}'.format(latitude = event_dict[key]['geolocation']['latitude'],
                                                                                                          longitude = event_dict[key]['geolocation']['longitude'])
                if 'asn' in event_dict[key]:
                    event_dict[key]['asn'] = str(event_dict[key]['asn'])

        # event indexing
        try:
            res = self.es.index(index=self.parameters.index, 
                                doc_type='event', 
                                body=event_dict)
        except elasticsearch.ElasticsearchException as e:
            self.logger.error('Event:\n{0}\nException:\n{1}'.format(json.dumps(event_dict), e))
            
        self.acknowledge_message()

if __name__ == "__main__":
    bot = ElasticSearch(sys.argv[1])
    bot.start()
