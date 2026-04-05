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
        self.vector_store.persist()

    def answer(self, question: str):
        # Simple similarity search to start with
        results = self.vector_store.similarity_search(question, k=3)
        if not results:
            return "Sorry, I dont have information about this question."

        # Combine the top results into a readable string
        context = "\n\n".join([doc.page_content for doc in results])
        return f"Based on my knowledge:\n\n{context}"

