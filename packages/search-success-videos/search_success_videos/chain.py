from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import ConfigurableField


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

client = QdrantClient(path="/home/sebastian/qdrant-dbs/bga-success-stories")

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