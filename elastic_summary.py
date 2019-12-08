#!/usr/bin/env python
# coding=utf-8

from elasticsearch import Elasticsearch

es = Elasticsearch("http://seal45.qa.lab.tlv.redhat.com:9200")

print("Count:\n{}\n".format(es.count()))
print("Info:\n{}\n".format(es.info()))

res = es.search(index="jenkins", body={"query": { "match": {"jobName": "util-artifacts-janitor-ovb-customized"} }})
print(res)
