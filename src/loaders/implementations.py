import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from .base import LoaderStrategy

class PDFLoaderStrategy(LoaderStrategy):
    def load(self, path: str):
        loader = PyPDFLoader(path)
        return loader.load()

class DirectoryLoaderStrategy(LoaderStrategy):
    def load(self, path: str):
        # This handles multiple files types in a foler
        loader = DirectoryLoader(path, glob="**/*.md", loader_cls=TextLoader)
        return loader.load()

def get_loader(path: str):
    if os.path.isdir(path):
        return DirectoryLoaderStrategy()
    elif path.lower().endswith(".pdf"):
        return PDFLoaderStrategy()
    else:
        raise ValueError("Unsupported path. Please provide a PDF or Folder.")

