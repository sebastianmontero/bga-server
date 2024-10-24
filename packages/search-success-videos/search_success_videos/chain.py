import os
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import ConfigurableField

qdrant_api_key = os.getenv("QDRANT_API_KEY")
# print("""QDRANT_API_KEY: """, qdrant_api_key)
if not qdrant_api_key:
    raise ValueError("QDRANT_API_KEY is not set")

qdrant_url = os.getenv("QDRANT_CLUSTER_URL")
if not qdrant_url:
    raise ValueError("QDRANT_CLUSTER_URL is not set")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, prefer_grpc=True)

qdrant_vector_store = QdrantVectorStore(
    client=client,
    collection_name="bga_success_stories",
    embedding=embeddings,
)

chain = qdrant_vector_store.as_retriever().configurable_fields(
    search_kwargs=ConfigurableField(
        id="search-parameters",
        name="search parameters",
        description="Set additional search parameters for the retriever",
    )
)


def get_industries() -> list[str]:
    industries = set ()
    offset = None
    while True:
        (points, offset) = client.scroll(collection_name="bga_success_stories", limit=1000, offset=offset)
        for point in points:
            # print(point)
            industry = point.payload.get('metadata', {}).get('industry')
            if industry:
                industries.add(industry)

        if not offset:
            break
    industries = list(industries)
    industries.sort()
    print(industries)
    return industries