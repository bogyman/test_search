class _Dict(dict):
    """
    can not use defaultdict
    Reversed index for terms
    """

    def save(self, document_hash, term):
        if term not in self:
            self[term] = {document_hash}
        else:
            self[term].add(document_hash)

    def search_term(self, term):
        return self.get(term)


class _Documents(dict):
    """
    documents storage
    """
    def save(self, document_hash, document):
        self[document_hash] = document

    def get_document(self, document_hash):
        return self.get(document_hash)


Dict = _Dict()
Documents = _Documents()
