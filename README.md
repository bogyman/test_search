Implemented system has 3 parts
- front: get htttp requests and return results
- node_manager: node management, sharding requests, transform input document and query to terms, calculate scores
- node: store reversed index, documents search document by term

API:
/index 
- force indexing process

/search?q=<q>
- return documents(if found) ordered by score
- q - words
- scoring by amount of words from query in document
