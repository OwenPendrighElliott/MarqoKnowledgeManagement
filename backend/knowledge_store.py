from typing import Union, Dict, List, Callable

import marqo


def default_chunker(document: str):
    return [{"text": document}]


class MarqoKnowledgeStore:
    def __init__(
        self,
        client: marqo.Client,
        index_name: str,
        document_chunker: Callable[[str], List[str]] = default_chunker,
    ) -> None:
        self._client = client
        self._index_name = index_name
        self._document_chunker = document_chunker

        try:
            self._client.create_index(self._index_name)
        except:
            print("Index exists")

    def query_for_content(
        self, query: Union[str, Dict[str, float]], content_var: str, limit: int = 5
    ):
        resp = self._client.index(self._index_name).search(q=query, limit=limit)
        knowledge = [res[content_var] for res in resp["hits"] if res["_score"] > 0.6]

        return knowledge

    def add_document(self, document):
        self._client.index(self._index_name).add_documents(self._document_chunker(document))

    def reset_index(self):
        self._client.delete_index(self._index_name)
        self._client.create_index(self._index_name)
