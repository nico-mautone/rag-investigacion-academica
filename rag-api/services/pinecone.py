from pinecone import Pinecone

from config import INDEX_NAME, PINECONE_API_KEY

class PineconeService:
    def __init__(self, api_key: str, index_name: str):
        # Initialize Pinecone client
        self.client = Pinecone(api_key=api_key)
        
        # Ensure index exists
        if not self.client.has_index(index_name):
            print("Pinecone Index not found.")
        self.index = self.client.Index(index_name)

    def get_embedding(self, text: str) -> list[float]:
        """Get embedding for a single text using pinecone's embedding endpoint."""
        response = self.client.inference.embed(
            model="multilingual-e5-large",
            inputs=[text],
            parameters={
                "input_type": "query"
            }
        )
        return response[0].values
    
    def get_similar_documents(self, query_vector: list[float], top_k: int = 3):
        """
        Get similar documents for a given query using Pinecone.
        
        Returns a list of dictionaries with metadata.
        """

        # Query the index
        response = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )

        # Gather results
        results = []
        for match in response.matches:
            meta = match.metadata
            results.append({
                "title": meta.get("title", ""),
                "abstract": meta.get("abstract", ""),
                "score": match.score  # optionally keep track of similarity score
            })
        return results

pinecone_service = PineconeService(api_key=PINECONE_API_KEY, index_name=INDEX_NAME)