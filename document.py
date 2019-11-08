#!/usr/bin/python
import json
import python_bitbankcc
from datetime import datetime
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch()
pub = python_bitbankcc.public()
json = pub.get_ticker('btc_jpy')

doc = {
    'close': int(json['last']),
    'volume': float(json['vol']),
    'timestamp': int(json['timestamp'])
}

res = es.index(index="btcjpy", id=1, body=doc)
print(res['result'])

res = es.get(index="btcjpy", id=1)
print(res['_source'])

