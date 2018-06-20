import os
import pickle
from elasticsearch import Elasticsearch

def load_data(file, credentials):
    
     """ Retrieve data from an Elasticsearch database
     
    # Arguments
        file: A file path specifying where the database should be saved or read from.
        credentials: A dictionary storing the parameters to pass to elasticsearch.Elasticsearch(). 
    # Returns
        A list of dictionaries.
    # References
        - https://gist.github.com/drorata/146ce50807d16fd4a6aa
    """
    
    if not os.path.exists(file):
        
        es = Elasticsearch(credentials['ES_HOST'], 
                           http_auth = (credentials['ES_USR'], credentials['ES_PWD']),
                           scheme = credentials['ES_SCHEME'], 
                           port = credentials['ES_PORT'])
        
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