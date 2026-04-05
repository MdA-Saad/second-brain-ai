import gradio as gr
import os
from src.loaders.implementations import get_loader
from src.engine import SecondBrainEngine
from dotenv import load_dotenv
load_dotenv() # this looks for the .env file and loads the hugging face TOKEN

engine=SecondBrainEngine()

def process_and_chat(file_path, question):
    if file_path and not engine.is_indexed(file_path):
        # using our strategy pattern via the Factory
        loader = get_loader(file_path)
        docs = loader.load(file_path)
        engine.ingest(docs)

    return engine.answer(question)

# Build the UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("AI Second Brain")

    with gr.Row():
        file_input = gr.File(label="Upload PDF or Folder (Zip)")
        question_input = gr.Textbox(label="Ask your brain")

    output_text = gr.Textbox(label="Response")
    submit_btn = gr.Button("Query System")

    submit_btn.click(fn=process_and_chat, inputs=[file_input, question_input], outputs=output_text)

if __name__=="__main__":
    demo.launch(server_name="0.0.0.0")
