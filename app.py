import os
import telebot
import google.generativeai as genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

bot = telebot.TeleBot(BOT_TOKEN)

# User memory store
user_memory = {}

# First welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
        "Assalamu Alaikum 🌿\n\n"
        "Ami ekta Powerful AI Bot 🤖\n"
        "Tumi ja jiggesh korba ami chesta korbo best answer dite.\n\n"
        "Cholo start kori 🚀"
    )

# Normal message handler with memory
@bot.message_handler(func=lambda message: True)
def reply(message):
    user_id = message.chat.id
    user_text = message.text

    try:
        # আগের memory থাকলে যোগ করো
        if user_id in user_memory:
            context = user_memory[user_id] + "\nUser: " + user_text
        else:
            context = user_text

        response = model.generate_content(context)
        ai_reply = response.text

        # নতুন memory save করো (limit 5 message)
        user_memory[user_id] = context + "\nAI: " + ai_reply
        if len(user_memory[user_id]) > 3000:
            user_memory[user_id] = user_memory[user_id][-3000:]

        bot.reply_to(message, ai_reply)

    except Exception as e:
        bot.reply_to(message, "Error hoise 😢")

print("Bot Running...")
bot.infinity_polling()
