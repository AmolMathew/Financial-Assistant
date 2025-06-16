from langchain_huggingface import HuggingFaceEmbeddings
EMBEDDINGS = HuggingFaceEmbeddings(model_name="thenlper/gte-base")
def embed_query(query: str):
    return EMBEDDINGS.embed_query(query)
