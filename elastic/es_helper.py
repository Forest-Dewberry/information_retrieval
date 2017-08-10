#
# Created by Umanga Bista.
#

import json
import config

def create_index(es_conn, index_name, settings_path = config.SETTINGS_PATH):
    '''
        reads a document from path
        input:
            - es_conn: elasticsearch connection object
            - index_name: name of index to create
            - settings_path: path to json w/ settings and mappings for index to create
        output: =>
            - None
    '''
    if es_conn.indices.exists(index_name):
        es_conn.indices.delete(index = index_name)
        print('index `{}` deleted'.format(index_name))
    with open(settings_path) as json_data:
        settings = json.load(json_data)
        es_conn.indices.create(index = index_name, ignore = 400, body = settings)
        print('index `{}` created'.format(index_name))

def extract_response(res):
    if res is not None:
        for hit in res['hits']['hits']:
            filename = hit["_source"]["filename"]
            score = hit["_score"]
            yield (filename, score)

def search(query_string, es_conn, index_name):
    '''
        searches for query_string with default search algorithm
        input:
            - query_string: a query
            - es_conn: elasticsearch connection
            - index_name: name of index
        output:
            - a generator of tuple (filename, score)

    '''
    res = es_conn.search(index = index_name,
        body = {
            "_source": [ "filename"],
            "query": {
                "query_string": {
                    "query": query_string,
                }
            }
        }
    )
    for hit in res['hits']['hits'][:n_hits]:
        filename = hit["_source"]["filename"]
        score = hit["_score"]
        yield (filename, score)

def get_tokens(query_string, es_conn, index_name):
    '''
        searches query_string on elasticsearch and returns tuples of (filename, term_vectors)
        # GET /comp4650-lab1-q1/doc/email01/_termvectors?fields=text
        input:
            - query_string: a query text
            - es_conn: elasticsearch connection
            - index_name: name of index
        output:
            - a generator of tuple (filename, term_vectors)

        description of output fields:
            - filename
            - term_vectors : a dct containing field_stats and a dict of tokens with their stats
    '''
    for filename, _ in search(query_string, es_conn, index_name):
        termvectors = es_conn.termvectors(index = config.INDEX_NAME,
                                    doc_type = config.DOC_TYPE,
                                    id = filename,
                                    field_statistics = True,
                                    fields = ['text'],
                                    term_statistics = True,
                                    positions = False,
                                    offsets = False,
                                    payloads = False
                                )
        # field_stats = termvectors["term_vectors"]["text"]["field_statistics"]
        # tokens = termvectors["term_vectors"]["text"]["terms"]
        yield filename, termvectors["term_vectors"]["text"]

def analyze_query(text, es_conn, index_name):
    '''
        analyzes any text with my_analyzer defined in es_settings.json
        input:
            - text: a query text
            - es_conn: elasticsearch connection
            - index_name: name of index
        output:
            - a list of tokens
    '''

    tokens = es_conn.indices.analyze(
        index = index_name,
        body = {"text": text},
        analyzer = 'my_analyzer')["tokens"]
    return [token_row["token"].encode('utf-8') for token_row in tokens]
