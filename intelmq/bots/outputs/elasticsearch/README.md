IntelMQ to ElasticSearch
===================

More information on ElasticSearch:
-------------------
https://www.elastic.co/products/elasticsearch

Installation:
-------------------
1. Install bot dependencies
`pip install elasticsearch`
or use predefined REQUIREMENTS file
`pip install -r intelmq/bots/outputs/elasticsearch/REQUIREMENTS`
2. Initialize your ElasticSearch index
`curl -vX PUT [localhost]:[9200]/[intelmq]/event -d @intelmq/bots/outputs/elasticsearch/intelmq.schema --header "Content-Type: application/json"`
