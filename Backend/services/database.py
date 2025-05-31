from pymilvus import MilvusClient


class DatabaseClient:
    """Singleton wrapper for the Milvus client."""

    _instance = None

    @classmethod
    def get_instance(cls, uri=None, token=None):
        """Return a shared Milvus client instance, creating one if necessary."""

        if cls._instance is None:
            if uri is None or token is None:
                raise ValueError(
                    "First call to get_instance must provide uri and token."
                )
            cls._instance = MilvusClient(uri=uri, token=token)
        return cls._instance
