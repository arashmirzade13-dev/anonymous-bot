from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import datetime

from config import BOT_TOKEN, ADMINS


# ساخت قالب پیام ناشناس
def build_anonymous_message(text, user_id):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    msg = (
        f"📩 *پیام ناشناس*\n"
        f"🆔 *کاربر:* `{user_id}`\n"
        f"📅 *تاریخ:* {date_str}\n"
        f"⏰ *ساعت:* {time_str}\n\n"
        f"*متن پیام:*\n"
        f"{text}"
    )
    return msg


# هندلر پیام‌ها
async def handle_message(update: Update, context):
    text = update.message.text
    user_id = update.message.from_user.id

    msg = build_anonymous_message(text, user_id)

    # ارسال پیام به مدیرها
    for admin in ADMINS:
        await context.bot.send_message(
            chat_id=admin,
            text=msg,
            parse_mode="Markdown"
        )

    # جواب به کاربر
    await update.message.reply_text("پیامت ارسال شد ✔️")


# ساخت اپلیکیشن ربات
def create_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    return app
