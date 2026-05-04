from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.database.vector_store import VectorStoreSingleton

class SecondBrainEngine:
    def __init__(self):
        self.vector_store = VectorStoreSingleton().get_db()
        self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )

    def ingest(self,documents):
        chunks = self.splitter.split_documents(documents)
        self.vector_store.add_documents(chunks)
        if hasattr(self.vector_store, 'persist'):
            self.vector_store.persist()

    def query(self, question: str):
        # Simple similarity search to start with
        results = self.vector_store.similarity_search(question, k=3)
        if not results:
            return {"answer": "No info found.", "contexts":[]}

        # Combine the top results into a readable string
        contexts=[doc.page_content for doc in results]
        answer=f"### Based on my knowledge:\n\n"+"\n\n".join(contexts)
        return {"answer": answer, "contexts": contexts}

