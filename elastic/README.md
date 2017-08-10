## Before you start

Before starting to work on this assignment, you should start 'elasticsarch'.

- to start elasticsearch, go to $ELASTICSEARCH_HOME/bin and enter command `./elasticsearch -d`.
- verify elasticsearch is running at `http://localhost:9200`


The demo code is written in python 2.7. If you are using python 3, we recommend you to use a [python virtual environment](https://docs.python.org/3/tutorial/venv.html). To run the demo code, you must install [python elasticsearch library](https://github.com/elastic/elasticsearch-py) which provide common ground for all Elasticsearch-related code in Python.

- install Python elasticsearch client. You can install this module with pip.

## running
The configurations are defined in file `config.py`. Before running make sure the configs are correct, especially the path to dataset, elasticsearch index_name and query_topics.

### 1. Indexing
To index the sample documents in `./ir_sample/documents`, run:

```
python es_index.py
```

### 2. Searching
To search queries from indexed documents, run:

```
python es_search_sample.py
```

It will print (`query`, `filename`, `score`) triples given the sample queries.

### 3. TREC_EVAL
TREC_EVAL will evaluate the performance of your search engine. To evaluate your search result, you first need two sets of files: the retrieved result file and the ground truth file.
Let's say your retrieval result is saved at `retrieved.txt` (see the detail formatting in assignment file), and the ground truth file is saved at `truth.qrels`. The performance of your retrieval can be measured via:

```
./trec_eval.9.0/trec_eval  truth.qrels retrieved.txt
```

`./trec_eval -h` will list all the options available.

Note that you should run `make` to build an excutable, `trec_eval`, before evaluating your results.

## Changing analyzers
The settings for analyzers is defined in file `es_settings_sample.json`. Try with different filters and tokenizers.
documentation for the analysis is found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html)

## Build your own search
To build your own_search, use function `get_tokens` inside `es_helper.py` to get a generator of tuples (filename, term_vectors). An example of term_vector is provided in file `example_term_vector.json`.

The details of term_vectors is found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-termvectors.html). Use this term_vectors to build your own search.

The output of your search should be in same format as described in the assignment handout, so that it can be feed directly to `trec_eval`.


## Miscellaneous

Optionally, you can also use kibana, which provides UI on top of elasticsearch. Visit [here](https://www.elastic.co/products/kibana) for details.
to start kibana, go to $KIBANA_HOME/bin and enter command `nohup kibana &`.
- verify kibana is running at `http://localhost:5601`
