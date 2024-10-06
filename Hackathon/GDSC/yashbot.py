import openai
import random

openai.api_key = "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"
model_engine = "text-davinci-002"

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

def get_response(message):
    try:
        prompt = f"Me: {message}\nBot:"
        bot_response = generate_response(prompt)
        return bot_response
    except Exception as e:
        print(e)
        return "I'm sorry, I encountered an error and could not generate a response."

def main():
    print("AI: Hi, how can I help you?")
    while True:
        user_input = input("You: ")
        bot_response = get_response(user_input)
        print(f"AI: {bot_response}")
        if "bye" in user_input.lower():
            print("AI: Bye!")
            break

if __name__ == "__main__":
    main()
