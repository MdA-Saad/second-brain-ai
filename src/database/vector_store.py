from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

class VectorStoreSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStoreSingleton, cls).__new__(cls)

            cls._instance.embeddings = HuggingFaceEmbeddings(
                    model_name="all-MiniLM-L6-v2"
                )

            persist_dir = os.path.join(os.getcwd(), "chroma_db")
            cls._instance.db = Chroma(
                    persist_directory=persist_dir,
                    embedding_function=cls._instance.embeddings
                )
        return cls._instance
    def get_db(self):
        return self.db

