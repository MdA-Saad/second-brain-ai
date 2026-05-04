import os
import json
from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import OllamaModel
from eval_logger import RAGLogger

from src.engine import SecondBrainEngine

os.environ["DEEPEVAL_PER_TASK_SECONDS_OVERRIDE"] = "600"

local_model = OllamaModel(model="phi3")
logger = RAGLogger(version="v1.0_Ollama_RAG", base_path="eval/logs")

def run_evaluation(query, actual_output, retrieval_context):
    # Define test case
    test_case = LLMTestCase(
            input=query,
            actual_output=actual_output,
            retrieval_context=retrieval_context
            )
    faith_metric = FaithfulnessMetric(threshold=0.7, model=local_model)
    rel_metric = AnswerRelevancyMetric(threshold=0.7,model=local_model)

    evaluate([test_case], metrics=[faith_metric, rel_metric])
    
    scores = {
            "context_relevance": 0,
            "faithfulness": faith_metric.score,
            "answer_relevance": rel_metric.score,
            "overall_comment": f"Reasoning: {faith_metric.reason}"
        }

    logger.log_iteration(
            query=query,
            response=actual_output,
            version="v1.0_Naive",
            retrieved_context=retrieval_context,
            scores=scores
        )

def run_bulk_eval():
    engine = SecondBrainEngine()

    # Load the golden set
    with open("eval_data/golden_set.json","r") as f:
        golden = json.load(f)

    for item in golden:
        query = item.get("input")
        print(f"\nEvaluating: {query}:")

        # Get the real response from the RAG
        result = engine.query(query)
        actual_output = result["answer"]
        retrieval_context = result["contexts"]

        run_evaluation(
                query=query,
                actual_output=actual_output,
                retrieval_context=retrieval_context
                )
if __name__=="__main__":
    run_bulk_eval()
