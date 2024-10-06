import telegram
from telegram.ext import Updater, MessageHandler, Filters
import openai

openai.api_key = "*********************************************"
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
        prompt = f"User: {message}\nBot:"
        bot_response = generate_response(prompt)
        return bot_response
    except Exception as e:
        print(e)
        return "I'm sorry, I encountered an error and could not generate a response."

def reply(update, context):
    user_input = update.message.text
    bot_response = get_response(user_input)
    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)

def main():
    bot = telegram.Bot(token='6003171836:AAG6-UmySDYxgc4JXIFpynTsZLoo5VtZS_s')
    updater = Updater(token='6003171836:AAG6-UmySDYxgc4JXIFpynTsZLoo5VtZS_s', use_context=True)
    dispatcher = updater.dispatcher
    message_handler = MessageHandler(Filters.text & (~Filters.command), reply)
    dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
