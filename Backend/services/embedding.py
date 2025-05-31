import cohere


class Embedding:
    """Uses Cohere to embed texts into float vectors."""

    def __init__(self, input_type, model="embed-v4.0", vector_dim=1024):
        """Initialize embedding client with model and vector configuration."""

        self.client = cohere.ClientV2()
        self.model = model
        self.input_type = input_type
        self.vector_dim = vector_dim

    def embed_texts(self, texts):
        """Embed a list of texts into vector representations."""

        batch_size = 96
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            res = self.client.embed(
                texts=batch,
                model=self.model,
                input_type=self.input_type,
                output_dimension=self.vector_dim,
                embedding_types=["float"],
            )
            all_embeddings.extend(res.embeddings.float)

        return all_embeddings
