import os
import json
from datetime import time, timedelta
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatMemberHandler,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "channels.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def track_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat and chat.type in ["group", "supergroup", "channel"]:
        data = load_data()
        if str(chat.id) not in data:
            data[str(chat.id)] = {}
            save_data(data)

async def send_weekly(context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    text = (
        "📢 Colaboración entre comunidades\n\n"
        "Únete a nuestro grupo:\n"
        "👉 https://t.me/+rrpTFx_84SQ2YTVk"
    )

    for chat_id in data.keys():
        try:
            msg = await context.bot.send_message(int(chat_id), text)
            context.job_queue.run_once(
                delete_message,
                when=timedelta(hours=12),
                data={
                    "chat_id": chat_id,
                    "message_id": msg.message_id
                }
            )
        except:
            pass

async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(
            chat_id=int(job.data["chat_id"]),
            message_id=job.data["message_id"]
        )
    except:
        pass

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(ChatMemberHandler(track_channels))

app.job_queue.run_daily(
    send_weekly,
    time=time(hour=12, minute=0)
)

app.run_polling()
