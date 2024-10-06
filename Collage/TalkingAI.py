import openai

import speech_recognition as sr
import pyttsx3

openai.api_key = "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"
model_engine = "text-babbage-001"
engine = pyttsx3.init()
r = sr.Recognizer()

def generate_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def get_response():
    try:
        with sr.Microphone() as source:
            print("Speak now!")
            audio = r.listen(source)
        user_input = r.recognize_google(audio)
        print("You said: " + user_input)
        prompt = f"Me: {user_input}\nAI:"
        bot_response = generate_response(prompt)
        return bot_response
    except Exception as e:
        print(e)
        return "I'm sorry,Please speak again."

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    speak("Hello, I am an AI currently i am in Atria Institute of Technology, I can talk like an human and i can answer the questions also.")
    while True:
        bot_response = get_response()
        speak(bot_response)
        print(f"AI: {bot_response}")
        if "bye" in bot_response.lower():
            speak("Bye!")
            break

if __name__ == "__main__":
    main()
