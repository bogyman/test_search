from node.storage import Documents, Dict

mapping = 'name'


def store_document(document_hash, document):
    Documents.save(document_hash, document)


def store_terms(document_hash, terms):
    for term in terms:
        Dict.save(document_hash, term)
