import openai
import random
import speech_recognition as sr
import pyttsx3

openai.api_key = "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"
model_engine = "text-davinci-002"
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
        prompt = f"Me: {user_input}\nBot:"
        bot_response = generate_response(prompt)
        return bot_response
    except Exception as e:
        print(e)
        return "I'm sorry, I encountered an error and could not generate a response."

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    speak("Hi, how can I help you?")
    while True:
        bot_response = get_response()
        speak(bot_response)
        print(f"Bot: {bot_response}")
        if "bye" in bot_response.lower():
            speak("Bye!")
            break

if __name__ == "__main__":
    main()
