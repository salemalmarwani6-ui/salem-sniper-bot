
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", "10000"))

searching = False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في SalemSniper 🎯\n\n"
        "المنصات المستهدفة:\n"
        "TikTok ✅\n"
        "Instagram ✅\n\n"
        "استخدم /help لمعرفة الأوامر."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - تشغيل البوت\n"
        "/help - المساعدة\n"
        "/platforms - عرض المنصات\n"
        "/search - تفعيل البحث\n"
        "/stop - إيقاف البحث\n"
        "/status - حالة النظام\n"
        "/results - عرض النتائج"
    )


async def platforms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "المنصات المستهدفة:\nTikTok\nInstagram"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global searching
    searching = True
    await update.message.reply_text(
        "تم تفعيل وضع البحث 🎯\n"
        "مصادر رصد البثوث لم يتم ربطها بعد."
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global searching
    searching = False
    await update.message.reply_text("تم إيقاف البحث.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = "مفعّل" if searching else "متوقف"
    await update.message.reply_text(
        f"حالة SalemSniper: يعمل\n"
        f"وضع البحث: {state}\n"
        "مصادر الرصد: لم يتم ربطها بعد."
    )


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "لا توجد نتائج حالياً. "
        "سيتم عرض النتائج بعد ربط مصادر الرصد."
    )


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    if not WEBHOOK_URL:
        raise RuntimeError("RENDER_EXTERNAL_URL is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("platforms", platforms))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("results", results))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
