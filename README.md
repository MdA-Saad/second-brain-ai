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
> I started with a "Naive RAG" system `vector_search->context->LLM`.

> "The system performs a**Linear Scan k-Nearest Neighbor** search. It projects the natural language query into an $n$-dimensional Hilbert space and utilizes the **Cosine Similarity** coefficient to compute the proximity between the query vector $\mathbf{q}$ and document vectors $\mathbf{d}$."
The formula for the similarity score is:
$$\text{score}(\mathbf{q}, \mathbf{d}) = \frac{\sum_{i=1}^{n} q_i d_i}{\sqrt{\sum_{i=1}^{n} q_i^2} \sqrt{\sum_{i=1}^{n} d_i^2}}$$

* **Result range:** $[ -1, 1 ]$. In text embeddings, it’s usually $[0, 1]$.
* **Intuition:** If the vectors point in the same direction, the score is $1$ (maximum similarity).

It retrieves a set of documents $D = \{ \mathbf{d}_1, \mathbf{d}_2, \dots, \mathbf{d}_m \}$ from your database and used `k=3`to select the top three indices where the similarity is highest.

$$\text{Results} = \text{arg}\max_{d \in D}^{k=3} \left( \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|} \right)$$

> "The `query` method implements a **Linear Scan k-Nearest Neighbor** search. It projects the natural language query into an $n$-dimensional Hilbert space and utilizes the **Cosine Similarity** coefficient to compute the proximity between the query vector $\mathbf{q}$ and document vectors $\mathbf{d}$."

> **Issue:** The model is finding the text based on similarity search without understanding the global context or intent.

## Versions log
- **Version 1.0:** I have built a basic similarity search based RAG model.
