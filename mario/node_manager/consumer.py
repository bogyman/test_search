import json
import uuid
from collections import defaultdict
from functools import partial
from itertools import groupby, chain

from node_manager.helpers import tockenizer, analizer, sharding, get_terms, get_node_by_document_hash
from node_manager.nodes_holder import NodesHolder
from utils import BaseMario, BaseMarioMixin
from utils.data_source import fetch_resources, get_nodes_offsets, get_nodes_tasks


class NodeManager(BaseMario):
    def __init__(self):
        self.queue_callbacks = (
            ('node__init', self.on_init_node, 'mario'),
            ('front__search', self.on_front_search, 'mario'),
            ('front__index', self.on_front_index, 'mario'),
        )

        super(NodeManager, self).__init__()

    @classmethod
    def on_init_node(cls, ch, method, props, body):
        data = json.loads(body)
        NodesHolder.add_node(data['id'])
        print(f"node {data} connected")

    def on_front_search(self, ch, method, props, body):
        print('on_front_search', body)
        data = json.loads(body)
        q = data['q']
        sm = SearchManager(channel=self.channel, reply_queue_name=props.reply_to)
        sm.init_search(q)

    def on_front_index(self, ch, method, props, body):
        print('on_front_index', body)
        im = IndexManager(channel=self.channel)
        im.init_indexing()


class SearchManager(BaseMarioMixin):

    def __init__(self, channel, reply_queue_name):
        super().__init__(channel)
        self.reply_queue_name = reply_queue_name
        self.terms_to_document_hashes = None
        self.documents_result = {}
        self.documents_order = None

    def init_search(self, q):
        """
        Make terms from query, sharing search requests by nodes
        :param q:
        :return:
        """
        result_queue_name = str(uuid.uuid4())
        tokens = tockenizer(q)
        terms = analizer(tokens)

        self.terms_to_document_hashes = {term: None for term in terms}

        for node, payload in sharding(NodesHolder.get_nodes(), terms).items():
            self.consume(result_queue_name, partial(self.gather_result, terms=terms))
            self.publish(
                payload=json.dumps(payload),
                queue_name=f"node__search__{node}",
                reply_to=result_queue_name
            )

    def gather_result(self, ch, method, props, body, terms=None):
        """
        Gather search result
        :param ch:
        :param method:
        :param props:
        :param body:
        :param terms:
        :return:
        """
        print("gather_result")
        terms_to_document_hashes = json.loads(body)['terms_to_document_hashes']

        for term, document_hashes in terms_to_document_hashes.items():
            if document_hashes:
                self.terms_to_document_hashes[term] = document_hashes
            else:
                del self.terms_to_document_hashes[term]

        if all(self.terms_to_document_hashes.values()):
            if self.terms_to_document_hashes:
                self.calculate_results(self.terms_to_document_hashes)
            else:
                # no results
                self.send_result(result={})

    def calculate_results(self, terms_to_document_hashes):
        """
        Calculate scores for each document
        :param terms_to_document_hashes:
        :return:
        """
        result_hashes = set.intersection(*[set(val.keys()) for val in terms_to_document_hashes.values()])
        result = defaultdict(list)
        for term, hash_to_position in terms_to_document_hashes.items():
            for _hash in result_hashes:
                result[_hash].append(hash_to_position[_hash])

        def _get_score(positions):
            if len(positions) == 1:
                return 0
            positions.sort()
            return positions[-1] - positions[0]

        print(result)

        self.documents_order = {_hash: _get_score(positions) for _hash, positions in result.items()}

        self.get_documents(self.documents_order.keys())

    def get_documents(self, document_hashes):
        """
        Get documents from nodes by document_hashes
        :param document_hashes:
        :return:
        """
        print('get_documents')
        for document_hash in document_hashes:
            self.documents_result[document_hash] = None

            result_queue_name = str(uuid.uuid4())
            node = get_node_by_document_hash(
                NodesHolder.get_nodes(),
                document_hash
            )

            self.consume(
                result_queue_name,
                partial(self.make_result, document_hash=document_hash)
            )

            self.publish(
                payload=json.dumps({'document_hash': document_hash}),
                queue_name=f"node__get_document__{node}",
                reply_to=result_queue_name
            )

    def make_result(self, ch, method, props, body, document_hash=None):
        """
        Gather all responses with documents, if all done, calculate score
        :param ch:
        :param method:
        :param props:
        :param body:
        :param document_hash:
        :return:
        """
        document = json.loads(body)
        if document:
            self.documents_result[document_hash] = document
        else:
            del self.documents_result[document_hash]

        if all(self.documents_result.values()):
            result = []
            for _document_hash, document in self.documents_result.items():
                result.append({
                    'document': document,
                    'score': self.documents_order[_document_hash]
                })
            result.sort(key=lambda x: x['score'])

            self.send_result(result)

    def send_result(self, result):
        """
        Return result to front
        :param result:
        :return:
        """
        self.publish(payload=json.dumps(result), queue_name=self.reply_queue_name)


class IndexManager(BaseMarioMixin):

    def init_indexing(self):
        """
        Get amout of work, split by nodes
        :return:
        """
        platforms_count = fetch_resources()
        nodes_offsets = get_nodes_offsets(NodesHolder, platforms_count)
        nodes_tasks = get_nodes_tasks(nodes_offsets)

        delay = 0
        for node, urls in nodes_tasks.items():
            for url in urls:
                self.make_task(node, url, delay)
                delay += 1000

    def make_task(self, node, url, delay):
        """
        Make task for fetching url by node
        :param node:
        :param url:
        :return:
        """
        task_queue_name = str(uuid.uuid4())
        self.consume(task_queue_name, self.index_documents)

        self.publish_delayed(
            payload=json.dumps({"url": url}),
            queue_name=f"node__get_resource__{node}",
            reply_to=task_queue_name,
            delay=delay
        )

    def index_documents(self, ch, method, props, body):
        """
        Split backet to documents, send for indexing
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        print('start_indexing')
        data = json.loads(body)
        for document in data:
            terms = get_terms(document)
            for node, payload in sharding(NodesHolder.get_nodes(), terms, document).items():
                self.publish(
                    payload=json.dumps(payload),
                    queue_name=f"node__index__{node}",
                )


