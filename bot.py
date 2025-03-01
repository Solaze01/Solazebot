from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import random
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")  # Load from environment variable

# Initialize the bot
app = Application.builder().token(TOKEN).build()

# Start command
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm Solaze Bot 🤖. Type /help to see what I can do.")

# Help command
async def help_command(update: Update, context):
    await update.message.reply_text("/news - Get latest news\n/quiz - Play a fun quiz\n/joke - Get a joke")

# Get news
async def get_news(update: Update, context):
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_NEWSAPI_KEY")
        news = response.json()
        article = random.choice(news["articles"])
        await update.message.reply_text(f"{article['title']}\n{article['url']}")
    except:
        await update.message.reply_text("❌ Sorry, I couldn't fetch news right now.")

# Fun quiz
quiz_questions = {
    "What is the capital of France?": "Paris",
    "What is 2 + 2?": "4",
    "What is the largest ocean?": "Pacific"
}

async def quiz(update: Update, context):
    question, answer = random.choice(list(quiz_questions.items()))
    context.user_data["answer"] = answer
    await update.message.reply_text(question)

async def check_answer(update: Update, context):
    user_answer = update.message.text
    correct_answer = context.user_data.get("answer")

    if correct_answer and user_answer.lower() == correct_answer.lower():
        await update.message.reply_text("✅ Correct!")
    else:
        await update.message.reply_text("❌ Wrong! Try again.")

# Joke command
async def joke(update: Update, context):
    jokes = ["Why don't programmers like nature? It has too many bugs!", 
             "Why do Java developers wear glasses? Because they don't C#!"]
    await update.message.reply_text(random.choice(jokes))

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("news", get_news))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))  # Check quiz answers

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
