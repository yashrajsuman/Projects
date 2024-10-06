import google.generativeai as genai

genai.configure(api_key="************************************")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

space=input("Do you have any space available for business operations?(enter in sqkm) : ")
skill=input("What skills or expertise do you possess? : ")
inventary=input("What physical items do you have in your inventory? : ")
#machinaries=input("Do you have any specialized equipment or machinery? :")
investement=input("What is your budget for starting a business? : ")

response = model.generate_content(f"You have to tell which business can I do, if I have all this: space-{space} sqkm, skill-{skill}, investment-{investement}, inventory={inventary}")


print(response.text)

