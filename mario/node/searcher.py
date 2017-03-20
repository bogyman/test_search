from itertools import zip_longest

from node.storage import Dict


def search_documents_hashes(terms):
    result = dict(zip_longest(terms, tuple()))

    for term in terms:
        document_hash_keys = Dict.search_term(term)

        if document_hash_keys:
            result[term] = document_hash_keys

    return result
