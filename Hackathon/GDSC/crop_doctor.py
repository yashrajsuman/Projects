import base64
import mimetypes
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

def generate():
    vertexai.init(project="learned-fusion-410613", location="us-central1")

    # Read the image file and convert it to base64
    image_path = "C:\\Users\\rajy9\\OneDrive\\Desktop\\stress-tolerant-rice-cuba.jpg"
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Determine the MIME type based on the file extension
    mime_type, _ = mimetypes.guess_type(image_path)

    # Create a Part object from the image data
    image1 = Part.from_data(data=image_data, mime_type=mime_type)

    model = GenerativeModel("gemini-pro-vision")
    responses = model.generate_content(
        [image1, "Which is this crop and what disease does it have"],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=True,
    )

    for response in responses:
        print(response.text, end="")

generate()
