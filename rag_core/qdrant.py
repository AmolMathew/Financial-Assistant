from qdrant_client import QdrantClient
from qdrant_client.http import models

QDRANT_HOST = '143.244.203.159'
QDRANT_PORT = 6333
QDRANT_API_KEY = 'your_qdrant_api_key'
COLLECTIONS = ['financial_docs_1','financial_docs_2', 'financial_docs_3', 'financial_docs_4', 'financial_docs_5']

client = QdrantClient(
    url=f"http://{QDRANT_HOST}:{QDRANT_PORT}",
    api_key=QDRANT_API_KEY,
    prefer_grpc=False,
    https=False
)

def search_qdrant(query_vector, top_k=5, filter_params=None):
    search_filter = None
    if filter_params:
        conditions = [
            models.FieldCondition(key=k, match=models.MatchValue(value=v))
            for k, v in filter_params.items()
        ]
        if conditions:
            search_filter = models.Filter(must=conditions)
    all_results = []
    for collection in COLLECTIONS:
        results = client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=top_k,
            query_filter=search_filter
        )
        for point in results:
            payload = point.payload
            all_results.append({
                "score": point.score,
                "collection": collection,
                "company": payload.get("company", {}),
                "chunk": payload.get("chunk", {}),
                "content": payload.get("chunk", {}).get("content", ""),
                "header": payload.get("chunk", {}).get("header", "")
            })
    return all_results
