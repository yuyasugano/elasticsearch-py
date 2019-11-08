#!/usr/bin/python
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch

size = 5

def print_search_stats(results):
    print("=" * 80)
    print("Total %d found in %dms" % (results["hits"]["total"]["value"], results["took"]))
    print("-" * 80)

def print_hits(results):
    " Simple utility function to print results of a search query. "
    print_search_stats(results)
    for hit in results["hits"]["hits"]:
        print("/%s/%s/%s close: %s, volume: %s" % (hit["_index"], hit["_type"], hit["_id"], hit["_source"]["close"], hit["_source"]["volume"]))
    print("=" * 80)
    print()

def print_sma(results):
    close = [results["hits"]["hits"][i]["_source"]["close"] for i in range(0, size)]
    print("%d seconds Simple Moving Avarage: %f" % (size, sum(close)/len(close)))

def main():
    # by default we connect to localhost:9200
    es = Elasticsearch()
    result= es.search(
        index="btcjpy",
        body={
          "size": size,
          "query": { "match_all": {} },
          "sort": { "timestamp": { "order": "desc" } }
        }
    )
    print_hits(result)
    print_sma(result)

if __name__ == '__main__':
    main()

