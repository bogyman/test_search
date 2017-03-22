Implemented system has 3 parts
- front: get htttp requests and return results
- node_manager: node management, sharding requests, transform input document and query to terms, calculate scores
- node: store reversed index, documents search document by term

API:
/index 
- force indexing process

/search?q=super mario
- return documents(if found) ordered by score
- q - words
--- scoring by amount of words from query in document ---



Updated:

- added timeout between requests to external API
- increased limit for request to external API
- added serialization of API response
- storing term position
- use logical AND for requested terms
- changed scoring by distance between terms



Can be scalled by start more than one Node service. Simple move to multi NodeManager.
Node instances should be memory opimized. NodeManager instances should be cpu opimized.
