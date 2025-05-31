from pymilvus import DataType
from Backend.services.database import DatabaseClient
import os


class DatabaseManager:
    """Handles schema creation, indexing, and data insertion for Milvus collections."""

    def __init__(self, vector_dim, max_len):
        """Initialize with vector dimension and max text length for schema."""

        self.client = DatabaseClient.get_instance(
            uri=os.environ.get("MILVUS_ZILLIZ_URI"),
            token=os.environ.get("MILVUS_ZILLIZ_TOKEN"),
        )
        self.vector_dim = vector_dim
        self.max_len = max_len
        self.schema = self._build_schema()
        self.index_params = self._build_index_params()

    def _build_schema(self):
        """Define and return the Milvus collection schema."""

        schema = self.client.create_schema(auto_id=True)
        schema.add_field("id", DataType.INT64, is_primary=True)
        schema.add_field("vector", DataType.FLOAT_VECTOR, dim=self.vector_dim)
        schema.add_field("text", DataType.VARCHAR, max_length=self.max_len)
        schema.add_field("weather", DataType.VARCHAR, max_length=50)
        schema.add_field("country", DataType.VARCHAR, max_length=50)

        return schema

    def _build_index_params(self):
        """Prepare indexing parameters for the vector field."""

        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="vector", index_type="AUTOINDEX", metric_type="COSINE"
        )
        return index_params

    def create_collection(self, collection_name):
        """Create a new collection with the defined schema and index."""

        self.client.create_collection(
            collection_name=collection_name,
            schema=self.schema,
            index_params=self.index_params,
        )

    def insert_data(self, collection_name, vectors, content, weather, country):
        """Insert document vectors and metadata into the specified collection."""

        data = [
            {"vector": vector, "text": text, "weather": weather, "country": country}
            for vector, text, weather, country in zip(
                vectors, content, weather, country
            )
        ]
        self.client.insert(collection_name=collection_name, data=data)

    def get_load_state(self, collection_name):
        """Return the loading state of the specified collection."""

        return self.client.get_load_state(collection_name=collection_name)
