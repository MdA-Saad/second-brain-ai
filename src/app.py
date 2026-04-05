import gradio as gr
from src.loaders.implementations import get_loader
from src.engine import SecondBrainEngine
from dotenv import load_dotenv

load_dotenv() # this looks for the .env file and loads the hugging face TOKEN

engine=SecondBrainEngine()

def process_and_chat(file_obj, question, history):
    if not file_obj:
        history.append({"role": "assistant","content": "Please upload a file first."})
        return history, ""
    
    # Use the loader strategy
    loader = get_loader(file_obj.name)
    docs = loader.load(file_obj.name)

    engine.ingest(docs)

    answer = engine.query(question)

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    return history,"" # Returns updated history and clear the input box

# Build the UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("AI Second Brain")

    chatbot = gr.Chatbot(label="Conversation")

    with gr.Row():
        file_input = gr.File(label="Upload PDF or Folder (Zip)")
        question_input = gr.Textbox(label="Ask your brain", placeholder="Type here...")

    submit_btn = gr.Button("Query System")

    submit_btn.click(
            fn=process_and_chat,
            inputs=[file_input, question_input, chatbot],
            outputs=[chatbot, question_input]
        )

if __name__=="__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
