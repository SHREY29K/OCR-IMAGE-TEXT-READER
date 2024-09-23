import easyocr
import gradio as gr
import json

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en', 'hi'])  # Supports Hindi and English

def ocr_image(image_path):
    # Use EasyOCR to extract text from the image file path
    result = reader.readtext(image_path, detail=0)
    # Returning in JSON Format
    return json.dumps({"extracted_text": result}, indent=4)

# OCR function with search keyword
def search_ocr(image_path, keyword):
    extracted_text = json.loads(ocr_image(image_path))["extracted_text"]
    
    # Search within the extracted text for the keyword
    matching_sections = [text for text in extracted_text if keyword.lower() in text.lower()]
    
    # Display results
    search_result = "\n".join(matching_sections) if matching_sections else "No matching results found."
    
    return extracted_text, search_result

# The main Gradio method
def create_interface():
    interface = gr.Interface(
        fn=search_ocr,
        inputs=[
            gr.Image(type="filepath", label="Upload Image"), 
            gr.Textbox(lines=1, placeholder="Enter keyword to search")
        ],
        outputs=[
            gr.Textbox(label="Extracted Text"),
            gr.Textbox(label="Search Result")
        ],
        title="Image Text Extraction and Search",
        description="Upload an image, extract text using OCR, and search within the extracted text."
    )
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(inline='False')

