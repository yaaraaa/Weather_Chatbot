import json
from Backend.services.embedding import Embedding
from Backend.services.indexing.db_manager import DatabaseManager


class DocumentIndexer:
    """Indexes structured data into Milvus after extracting content and embeddings."""

    def __init__(self, file_path):
        """Initialize with the path to the structured JSON data."""

        self.file_path = file_path

    def _load(self):
        """Load and get weather, activity, and clothing data from the file."""

        content = []
        weather = []
        country = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for weather_entry in data["weather_types"]:
            for country_info in weather_entry["countries"]:
                activities = f"Outdoor Activities: {country_info['outdoor_activities']}"
                clothing = (
                    f"Appropriate Clothing: {country_info['appropriate_clothing']}"
                )

                weather_lower = weather_entry["weather"].lower()
                country_lower = country_info["country"].lower()

                content.append(activities)
                weather.append(weather_lower)
                country.append(country_lower)

                content.append(clothing)
                weather.append(weather_lower)
                country.append(country_lower)

        return content, weather, country

    def index(self, session_id):
        """Embed and index data into a new Milvus collection."""

        content, weather, country = self._load()
        max_length = max(len(text) for text in content)

        embedding = Embedding(input_type="search_document")
        vectors = embedding.embed_texts(content)

        milvus_handler = DatabaseManager(
            vector_dim=embedding.vector_dim, max_len=max_length
        )

        milvus_handler.create_collection(session_id)
        milvus_handler.insert_data(session_id, vectors, content, weather, country)

        load_state = milvus_handler.get_load_state(session_id)
        return load_state
