from transformers import pipeline
import gradio as gr  # Import Gradio

# Initialize the translation pipeline with a specific model
translation_pipeline = pipeline('translation_en_to_de', model="Helsinki-NLP/opus-mt-en-de")

# Define the translation function
def translate_transformer(from_text):
    result = translation_pipeline(from_text, clean_up_tokenization_spaces=True)
    return result[0]['translation_text']

# Create the Gradio interface
interface = gr.Interface(
    fn=translate_transformer, 
    inputs=gr.components.Textbox(lines=2, placeholder='Text to Translate'),
    outputs=gr.components.Textbox()
)

# Launch the Gradio interface
# Set share=True if you want to create a public link
interface.launch(share=True)
