import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Fetch token and links from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your bot token
AFFILIATE_LINK = os.getenv("AFFILIATE_LINK")  # Your affiliate link
EBOOK_URL = os.getenv("EBOOK_URL")  # Your eBook URL

# Track user progress
user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎁 Get FREE Python eBooks & Courses!\n\n"
        "Send /ebook to get started!"
    )

async def request_ebook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_progress[user_id] = 0
    await update.message.reply_text(
        f"🔑 To unlock your FREE Python eBook:\n\n"
        f"1. Share this link with 3 friends:\n{AFFILIATE_LINK}\n"
        f"2. Send me a screenshot after sharing!"
    )

async def track_shares(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Check if user sent the affiliate link
    if AFFILIATE_LINK in text:
        if user_id not in user_progress:
            user_progress[user_id] = 0
        
        user_progress[user_id] += 1

        if user_progress[user_id] >= 3:
            await update.message.reply_text(
                "✅ Success! Download your FREE eBook:\n" + EBOOK_URL
            )
            del user_progress[user_id]
        else:
            await update.message.reply_text(
                f"⚠️ {3 - user_progress[user_id]} shares remaining!"
            )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ebook", request_ebook))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_shares))

    # Start bot
    logging.info("Bot is running...")
    app.run_polling()
