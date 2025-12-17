import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = set()

async def detect_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat and chat.type in ["channel", "supergroup"]:
        CHANNELS.add(chat.id)

async def weekly_spam(context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📢 Colaboración entre comunidades\n\n"
        "Únete a nuestro grupo:\n"
        "👉 https://t.me/TU_GRUPO"
    )
    for chat_id in CHANNELS:
        try:
            await context.bot.send_message(chat_id, message)
        except:
            pass

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(ChatMemberHandler(detect_bot_added))

scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: app.bot.loop.create_task(weekly_spam(app.bot)),
    'interval',
    weeks=1
)
scheduler.start()

app.run_polling()
