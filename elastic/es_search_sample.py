#
# Created by Umanga Bista.
#

import config
from io import open
import re, json
from elasticsearch import Elasticsearch
from es_helper import analyze_query, search, extract_response

def create_text_file(query, extra_Q0_field, match, rank, rounded, name_IR_system):
    print(query, extra_Q0_field, match, rank, rounded, name_IR_system)
    retrieved_text = open("retrieved.txt", "w")
    retrieved_text.write(query)
    retrieved_text.close()

def print_result(query, res):
    # retrieved_text = open("retrieved.txt", "w")
    name_IR_system = config.MY_NAME
    extra_Q0_field = "Q0"
    matches = extract_response(res)
    if matches is not None:
        with open("retrieved.txt", "a") as retrieved_text:
            rank = 0
            for match in sorted(matches, key = lambda x: -x[1]):
                output = query + " " + str(extra_Q0_field) + " " + str(match[0]) + " " + str(rank) + " " + str(round(match[1],2)) + " " + name_IR_system + "\n"
                retrieved_text.write(output)
                print('{}, {}, {}, {}, {}, {}'.format(
                    query,
                    extra_Q0_field, #extra field not used anymore
                    match[0], # filename
                    rank, # rank
                    str(round(match[1],2)), # score
                    name_IR_system, # name of the IR system
                ))
                rank+=1

        retrieved_text.close()

def read_topics():
    query_topics_dict = {}
    file_name = config.QUERY_TOPICS_PATH
    file_object = open(file_name,"r")
    for item in file_object.readlines():
        parts = item.split()
        key = parts[0]
        parts.pop(0)
        string_query = ' '.join(parts)
        string_query_lower_case = string_query.lower()
        query_topics_dict[key] = string_query_lower_case
    return query_topics_dict

def main():
    es_conn = Elasticsearch(config.ES_HOSTS)
    # Elasticsearch Query grammar can be found here:
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
    # To understand score of the result, check:
    # https://www.elastic.co/guide/en/elasticsearch/guide/current/relevance-intro.html#explain
    text_file = open("retrieved.txt", "w")

    for key, value in read_topics().items():
        individual_topic = str(value)
        res = es_conn.search(index = config.INDEX_NAME,
            body={
                  "_source": ["filename"],
                  "query": {
                    "bool": {
                      "must": [
                        {
                          "match": {"text": individual_topic}
                        }
                      ]
                    }
                  }
                }
            )
        print_result(key, res)

    # Boolean Query "Obama"
    # res = es_conn.search(index = config.INDEX_NAME,
    #     body={
    #           "_source": ["filename"],
    #           "query": {
    #             "bool": {
    #               "must": [
    #                 {
    #                   "match": {"text": "Obama"}
    #                 }
    #               ]
    #             }
    #           }
    #         }
    #     )
    # print_result("Obama", res)

    # # Boolean Query "Obama AND Hillary"
    # res = es_conn.search(index = config.INDEX_NAME,
    #     body={
    #           "_source": ["filename"],
    #           "query": {
    #             "match" : {
    #               "text" : {
    #                 "query" : "Obama Hillary",
    #                 "operator" : "and"
    #               }
    #             }
    #           }
    #         }
    #     )
    # print_result("Obama AND Hillary", res)
    #
    # # Boolean Query "Obama BUT Hillary"
    # res = es_conn.search(index = config.INDEX_NAME,
    #     body={
    #           "_source": ["filename"],
    #           "query": {
    #             "bool": {
    #               "must": [
    #                 {
    #                     "match": {"text": "Obama"}
    #                 }
    #               ],
    #               "must_not":[
    #                 {
    #                     "match": {"text": "Hillary"}
    #                 }
    #               ]
    #             }
    #           }
    #         }
    #     )
    # print_result("Obama BUT Hillary", res)
    #
    # # Boolean Query "Obama OR Hillary"
    # # default is OR
    # res = es_conn.search(index = config.INDEX_NAME,
    #     body={
    #           "_source": ["filename"],
    #           "query": {
    #             "match" : {
    #               "text" : {
    #                 "query" : "Obama Hillary",
    #               }
    #             }
    #           }
    #         }
    #     )
    # print_result("Obama OR Hillary", res)

if __name__ == '__main__':
    main()
