#!/usr/bin/python
import json
import time
import python_bitbankcc
from datetime import datetime
from elasticsearch import Elasticsearch

def get_ticker(pub):
    ret = pub.get_ticker('btc_jpy')
    return ret

def main():
    # by default we connect to localhost:9200
    es = Elasticsearch()
    pub = python_bitbankcc.public()

    while True:
        # every second we record cvt data
        for i in range(60):
            try:
                ret = get_ticker(pub)

                doc = {
                    'close': int(ret['last']),
                    'volume': float(ret['vol']),
                    'timestamp': int(ret['timestamp'])
                }

                print("----------------------------------------------------------------------")
                print(json.dumps(doc, indent=4, separators=(',', ': ')))
            except Exception as e:
                print("Error occurred: {}".format(e))

            try:
                res = es.index(index="btcjpy", id=i+1, body=doc)
                print("----------------------------------------------------------------------")
                print("Elasticsearch collected a second data: {}".format(res['result']))
            except Exception as e:
                print("Error occurred: {}".format(e))
            time.sleep(1)

if __name__ == '__main__':
    main()

