os.environ["DEEPEVAL_PER_TASK_TIMEOUT_SECONDS_OVERRIDE"] = "600"
os.environ["DEEPEVAL_VERBOSE_MODE"] = "1"

from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig
from deepeval.models import OllamaModel
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from deepeval.models import DeepEvalBaseEmbeddingModel
from dotenv import load_dotenv
import os

load_dotenv() # this is loading the fake key to bypass the openAI api key not configured error

class LocalEmbedder(DeepEvalBaseEmbeddingModel):
    """
    Custom Ollama model wrapper for Deepeval that bypasses OpenAI API key requirements.
    """
    def __init__(self, model_name="mxbai-embed-large"):
        self.model_name=model_name
        self.model = OllamaEmbeddings(model=model_name)

    def load_model(self):
        return self.model
    
    def get_model_name(self):
        return self.model_name

    def embed_text(self, text:str):
        return self.model.embed_query(text)

    def embed_texts(self, texts: list[str]):
        return self.model.embed_documents(texts)

    async def a_embed_text(self, text: str):
        return await self.model.aembed_query(text)

    async def a_embed_texts(self, texts: list[str]):
        return await self.model.aembed_documents(texts)


def generate_data():
    pdf_path='/home/saad/Documents/Projects/second-brain-ai/data/WEF_Global_Risks_Report_2026.pdf'
    
    # Manual extraction
    print("Extracting text from PDF")
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()

    # Chunking
    # 1200 characters is the sweet spor for Llama3.1 to generate 1 good question
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )
    chunks = text_splitter.split_documents(docs)

    # We take the first 15 meaningful chunks to ensure the process isn't too slow
    # DeepEval expects a list of lists: [[chunk1], [chunk2],.....]
    prepared_contexts = [[c.page_content] for c in chunks if len(c.page_content) > 400][:2]

    print(f" Extracted {len(prepared_contexts)} high quality contexts.")
    local_model = OllamaModel(model="llama3.1")
    local_embedder = LocalEmbedder(model_name="mxbai-embed-large")
    
    synthesizer = Synthesizer(model=local_model)

    os.makedirs("./eval_data", exist_ok=True)
    
    print("Starting synthesis... (This might take a few minutes with local Ollama)")
    
    goldens = synthesizer.generate_goldens_from_contexts(
            contexts=prepared_contexts,
            include_expected_output=True, 
            max_goldens_per_context=1,
        )
    
    if goldens:
        synthesizer.save_as(file_type='json', directory="./eval_data", file_name="golden_set")
        print(f"Successfully generated {len(goldens)} questions.")
    else:
        print("Wait! No questions were generated. Check your Ollama logs.")


if __name__ == "__main__":
    generate_data()
