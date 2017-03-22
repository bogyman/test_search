from node.storage import Documents, Dict

mapping = 'name'


def store_document(document_hash, document):
    Documents.save(document_hash, document)


def store_terms(document_hash, terms):
    for position, term in enumerate(terms):
        Dict.save((document_hash, position), term)


# should something like serializer
def make_document(item):
    return {
        'deck': item['deck'],
        'image': item['image'] and item['image'].get('icon_url'),
        'name': item['name'],
        'platforms': [pl['name'] for pl in item['platforms']],
        'site_detail_url': item['site_detail_url']
    }
