from Backend.services.database import DatabaseClient
from Backend.services import app_state
from Backend.services.embedding import Embedding
from langchain_core.tools import tool
from typing import Annotated
import os


@tool
def search_knowledge_base(
    query: Annotated[str, "The user question or search query."],
    weather: Annotated[
        str,
        "The weather conditions of the country the user mentioned, which is a value from (sunny, rainy, snowy, windy, cloudy).",
    ],
    country: Annotated[str, "The country that the user is staying at or going to."],
    top_k: Annotated[
        int,
        "The top k entries to retrieve, value should not be below 2 and should not exceed 5.",
    ] = 5,
) -> str:
    """
    Searches a vector-based knowledge base for the most relevant entries based on a text query and metadata filters.
    """

    top_k = int(top_k)

    client = DatabaseClient.get_instance(
        uri=os.environ.get("MILVUS_ZILLIZ_URI"),
        token=os.environ.get("MILVUS_ZILLIZ_TOKEN"),
    )

    embedding = Embedding(input_type="search_query")
    query_vectors = embedding.embed_texts([query])

    expr = f"weather LIKE '%{weather.lower()}%' AND country LIKE '%{country.lower()}%'"

    results = client.search(
        collection_name=app_state.collection_name,
        data=query_vectors,
        filter=expr,
        output_fields=["id", "text", "weather", "country"],
        limit=top_k,
        search_params={"metric_type": "COSINE"},
    )

    final = "\n".join([item["entity"]["text"] for item in results[0]])

    return final
