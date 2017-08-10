#
# Created by Umanga Bista.
#

import os
from collections import namedtuple
from io import open

## A document class with following attributes
## filename: document filename
## text: body of documment
## path: path of document
Doc = namedtuple('Doc', 'filename path text')

def read_doc(doc_path, encoding):
    '''
        reads a document from path
        input:
            - doc_path : path of document
            - encoding: encoding
        output: =>
            - doc: instance of Doc namedtuple
    '''
    filename = doc_path.split('/')[-1]
    fp = open(doc_path, 'r', encoding = encoding)
    text = fp.read().strip()
    fp.close()
    return Doc(filename = filename, text = text, path = doc_path)

def read_dataset(path, encoding = "ISO-8859-1"):
    '''
        reads multiple documents from path
        input:
            - doc_path : path of document
            - encoding: encoding
        output: =>
            - docs: instances of Doc namedtuple returned as generator
    '''
    for root, dirs, files in os.walk(path):
        for doc_path in files:
            yield read_doc(root + '/' + doc_path, encoding)

def main():
    # path = '../data/gov-test-collection/documents'
    path = '../data/lab1-q1-test-collection/documents'
    dataset = read_dataset(path)
    while True:
        try:
            item = next(dataset)
            print(item.id, item.category)
        except StopIteration:
            # exhausted, handle this case
            print('finisded')
            break

if __name__ == '__main__':
    main()
