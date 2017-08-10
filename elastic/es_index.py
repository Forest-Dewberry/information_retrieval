#
# Created by Umanga Bista.
#

from elasticsearch import Elasticsearch
from data import read_dataset
import config
from es_helper import create_index

def main():
    ## create an es client
    es_conn = Elasticsearch(config.ES_HOSTS, timeout=30)
    ## create the index if it doesn't exist
    create_index(es_conn = es_conn, index_name = config.INDEX_NAME)
    dataset = read_dataset(config.DOCS_PATH)
    counter_read, counter_idx_failed = 0, 0 ## counters

    while True:
        try:
            doc = next(dataset)
            res = es_conn.index(
                index = config.INDEX_NAME,
                doc_type = config.DOC_TYPE,
                id = doc.filename,
                body = doc._asdict())
            counter_read += 1

            if counter_read % config.PRINT_EVERY == 0:
                print('indexed {} documents'.format(counter_read))

            if not res['created']:
                print('indexing `{}` failed'.format(doc.path))
                counter_idx_failed += 1

        except StopIteration:
            print('finished reading docs from `{}`'.format(config.DOCS_PATH))
            break

    print('indexed {} docs to index `{}`, failed to index {} docs'.format(
        counter_read,
        config.INDEX_NAME,
        counter_idx_failed
    ))

if __name__ == '__main__':
    main()
