import json
import os
from datetime import datetime

class RAGLogger:
    def __init__(self, version="v1.0", base_path="eval/logs"):
        self.version = version
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_version = version.replace(" ", "_").replace(".","_")
        self.filename = f"{base_path}/{safe_version}_{date_str}.json
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        # Initialize the file if doesn't exist
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size==0:
            with open(self.filename, 'w') as f:
                json.dump([],f)
    
    def log_iteration(self, query, response, version, retrieved_context, scores=None):
        """
        Saves a single RAG interaction and its evaluation.

        :param query: The user input
        :param reponse: The LLM output
        :param version: e.g., "v1.0_Naive", "v1.1_Rewriter"
        :param retrieved_context: List of strings or IDs of the chunks retrieved
        :param scores: Dictionary containing RAG Triad metrics (0-5)
        """

        # Default scores if you haven't rated it yet
        if scores is None: 
            scores = {
                    "context_relevance": 0,
                    "faithfulness": 0,
                    "answer_relevance": 0,
                    "overall_comment": ""
                }
        entry = {
                "timestamp": datetime.now().isoformat(),
                "version": version,
                "query": query,
                "response": response,
                "retrieved_context": retrieved_context,
                "evaluation": scores,
                # Calculate a quick mean score for the "Big Brain" summary
                "mean_score": sum(v for k, v in scores.items() if isinstance(v, (int, float))) / 3
            }

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            data.append(entry)
            with open(self.filename, 'w') as f:
                json.dump(data,f, indent=4)
            print(f"Logged entry for {version}. Mean Score: {entry['mean_score']:.2f}")
            print(f"Successfully logged query to : {self.filename}")
        except Exception as e:
            print(f"Error logging to JSON: {e}")



