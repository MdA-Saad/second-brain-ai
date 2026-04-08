#  Second Brain AI
> **Transform your PDFs into an interactive knowledge base using RAG.**

###  Features
* **Semantic Search:** Finds meaning, not just keywords.
* **Dockerized:** One command to run anywhere.
* **Powered by uv:** Blazing fast dependency management.

### Tech Stack
- **Logic:** Python 3.11, LangChain
- **UI:** Gradio
- **Database:** ChromaDB (Vector Store)
- **Deployment:** Docker

### Local Setup
1. Clone the repo.
2. Create a `.env` file with your `HF_TOKEN`.
3. Run `uv run python -m src.app`.

## Technical Architecture
### **Version 1.0**
-- I starded with a basic `vector_search->context->LLM` pipeline.
-- Issue: The model is finding the text based on similarity search without understanding the global context or intent.

## Versions log
- **Version 1.0:** I have built a basic similarity search based RAG model.
