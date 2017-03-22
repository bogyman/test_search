import hashlib
import re

from collections import defaultdict


def tockenizer(q):
    return re.split(r'[\W]+', q)


def analizer(tokens):
    return [token.lower() for token in tokens]


def get_mapped(document):
    return document['name']


def get_document_hash(document):
    return hashlib.md5(get_mapped(document).encode()).hexdigest()


def get_node_by_document_hash(nodes, document_hash):
    return nodes[sum([ord(c) for c in document_hash]) % len(nodes)]


def get_node_by_term(nodes, term):
    """
    Sharding for full word search
    :param nodes:
    :param term:
    :return:
    """
    return nodes[sum([ord(c) for c in term]) % len(nodes)]


def sharding(nodes, terms, document=None):
    """
    Split storing documents and terms by nodes
    :param nodes:
    :param terms:
    :param document:
    :return:
    """
    shards = defaultdict(lambda: defaultdict(list))
    document_hash = None

    if document:
        document_hash = get_document_hash(document)
        node = get_node_by_document_hash(nodes, document_hash)
        shards[node]['document'] = document
        shards[node]['document_hash'] = document_hash

    for term in terms:
        shards[get_node_by_term(nodes, term)]['terms'].append(term)
        shards[get_node_by_term(nodes, term)]['document_hash'] = document_hash

    return shards


def get_terms(document):
    """
    Make terms form document
    :param document:
    :return:
    """
    q = get_mapped(document)
    tokens = tockenizer(q)
    terms = analizer(tokens)

    return terms
