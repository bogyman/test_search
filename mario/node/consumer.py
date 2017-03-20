import json

from node import NODE_ID
from node.indexer import store_document
from node.indexer import store_terms
from node.searcher import search_documents_hashes
from node.storage import Documents
from utils import BaseMario
from utils.data_source import get_resource


class Node(BaseMario):
    def __init__(self):
        self.queue_callbacks = (
            (f'node__index__{NODE_ID}', self.on_index),
            (f'node__search__{NODE_ID}', self.on_search),
            (f'node__get_resource__{NODE_ID}', self.on_get_resource),
            (f'node__get_document__{NODE_ID}', self.on_get_document)
        )

        super(Node, self).__init__()

    def on_index(self, ch, method, props, body):
        print('indexing')

        data = json.loads(body)

        document = data.get('document')
        terms = data.get('terms')
        document_hash = data.get('document_hash')

        if document and document_hash:
            store_document(document_hash, document)

        if terms:
            store_terms(document_hash, terms)

    def on_search(self, ch, method, props, body):
        data = json.loads(body)
        terms_to_document_hashes = search_documents_hashes(data['terms'])
        print(terms_to_document_hashes)
        # hack for json.dumps
        terms_to_document_hashes = {
            term: document_hashes and list(document_hashes)
            for term, document_hashes in terms_to_document_hashes.items()
        }

        self.publish(props.reply_to, json.dumps({
            'terms_to_document_hashes': terms_to_document_hashes
        }))

    def on_get_resource(self, ch, method, props, body):
        print('on_get_resource')
        data = json.loads(body)
        res = get_resource(data['url'])

        self.publish(props.reply_to, json.dumps(res))

    def on_get_document(self, ch, method, props, body):
        print('on_get_document')
        data = json.loads(body)
        document_hash = data['document_hash']
        document = Documents.get_document(document_hash)

        self.publish(props.reply_to, json.dumps(document))

