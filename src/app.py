import gradio as gr
from src.loaders.implementations import get_loader
from src.engine import SecondBrainEngine
from eval.eval_logger import  RAGLogger
from dotenv import load_dotenv

load_dotenv() # this looks for the .env file and loads the hugging face TOKEN
engine=SecondBrainEngine()

VERSION = "v1.0_Stage1_Pure_Retrieval"
logger = RAGLogger(version=VERSION)

def process_and_chat(file_obj, question,model_choice, history):
    if not file_obj:
        history.append({"role": "assistant","content": "Please upload a file first."})
        return history, ""
    
    # Use the loader strategy
    loader = get_loader(file_obj.name)
    docs = loader.load(file_obj.name)
    engine.ingest(docs)
    response  = engine.query(question)

    answer = response.get("answer", response) if isinstance(response, dict) else response
    context = response.get("context", []) if isinstance(response, dict) else ["context retrieval not implemented" ]


    formatted_answer = f"**[Model: {model_choice}]**\n\n{answer}"

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": formatted_answer})
    logger.log_iteration(
        query=question,
        response=answer,
        version=VERSION,
        retrieved_context=context
    )
    return history,"" # Returns updated history and clear the input box

# Custom CSS
custom_css = """
.gradio-container { font-family: 'Inter", sans-serif; }
.message-row { margin-bottom: 10px; }
"""
# Building UI
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("# AI Second Brain")

    with gr.Row():
        # Left Column: Configuration
        with gr.Column(scale=1):
            file_input = gr.File(label="1. Upload Knowledge", file_types=[".pdf", ".zip"])
            model_dropdown = gr.Dropdown(
                    choices=["Mistral-7B", "Llama-3-8B", "Phi-3-Mini"],
                    value="Mistral-7B",
                    label="2. Select AI Model"
                )
            clear_btn = gr.Button("Clear Chat", variant="stop")

    with gr.Column(scale=2):
        chatbot = gr.Chatbot(label="Conversation", height=500)
        
        with gr.Row():
            question_input = gr.Textbox(
                    label="Ask a question",
                    placeholder="Type here and press Enter...",
                    scale=4
                )
            submit_btn = gr.Button("Send", variant="primary", scale=1)

# Action for enter button
    submit_event = {
            "fn": process_and_chat,
            "inputs": [file_input, question_input, model_dropdown, chatbot],
            "outputs": [chatbot, question_input]
        }
    submit_btn.click(**submit_event)
    question_input.submit(**submit_event)

if __name__=="__main__":
    demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            theme=gr.themes.Soft(),
            css=custom_css
        )
