import os
import pickle
from elasticsearch import Elasticsearch

def load_data(file):
    if not os.path.exists(file):
        es = Elasticsearch(['35.199.37.111'], http_auth = ('mode', '&c43C*NwJspZP6D%'),
                           scheme = "http", port = 9200)
        'taken from https://gist.github.com/drorata/146ce50807d16fd4a6aa'
        page = es.search(scroll = '2m', size = 10000, body = {})
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']
        list_items = []
        while (scroll_size > 0):
            page = es.scroll(scroll_id = sid, scroll = '2m')
            list_items += page['hits']['hits']
            sid = page['_scroll_id']
            scroll_size = len(page['hits']['hits'])
        with open(file, 'wb') as fp:
            pickle.dump(list_items, fp)
    else:
        with open (file, 'rb') as fp:
            list_items = pickle.load(fp)
    return list_items