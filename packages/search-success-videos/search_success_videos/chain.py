from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

client = QdrantClient(path="/home/sebastian/qdrant-dbs/bga-success-stories")

qdrant_vector_store = QdrantVectorStore(
    client=client,
    collection_name="bga_success_stories",
    embedding=embeddings,
)

chain = qdrant_vector_store.as_retriever()
