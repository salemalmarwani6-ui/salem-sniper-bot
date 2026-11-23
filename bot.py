import os
import logging
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from scheduler import start_scheduler
from database import initialize, get_results
from config import SEARCH_INTERVAL, MIN_CONFIDENCE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", "10000"))

search_task = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في SalemSniper 🎯\n\n"
        "TikTok ✅\n"
        "Instagram ✅\n\n"
        "استخدم /help لمعرفة الأوامر."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - تشغيل البوت\n"
        "/help - المساعدة\n"
        "/platforms - المنصات\n"
        "/search - تشغيل البحث\n"
        "/stop - إيقاف البحث\n"
        "/status - حالة النظام\n"
        "/results - عرض النتائج"
    )


async def platforms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "المنصات المعتمدة:\n"
        "TikTok ✅\n"
        "Instagram ✅"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global search_task

    if search_task and not search_task.done():
        await update.message.reply_text("البحث يعمل بالفعل.")
        return

    search_task = asyncio.create_task(start_scheduler())

    await update.message.reply_text(
        "تم تشغيل محرك SalemSniper 🎯\n\n"
        "مستوى البحث: Maximum\n"
        "التنبيهات: Confirmed Only\n"
        f"الفاصل الزمني: {SEARCH_INTERVAL} ثانية\n"
        f"حد الثقة: {MIN_CONFIDENCE}\n\n"
        "بدأت دورة البحث."
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global search_task

    if search_task and not search_task.done():
        search_task.cancel()

        try:
            await search_task
        except asyncio.CancelledError:
            pass

        search_task = None

        await update.message.reply_text("تم إيقاف محرك البحث.")
    else:
        await update.message.reply_text("محرك البحث متوقف بالفعل.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    running = search_task is not None and not search_task.done()

    await update.message.reply_text(
        "SalemSniper Status 🎯\n\n"
        f"البوت: يعمل\n"
        f"محرك البحث: {'يعمل' if running else 'متوقف'}\n"
        "TikTok: مهيأ\n"
        "Instagram: مهيأ\n"
        "Search Level: Maximum\n"
        "Alert Mode: Confirmed Only\n"
        f"Interval: {SEARCH_INTERVAL} seconds"
    )


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    initialize()
    records = get_results(10)

    if not records:
        await update.message.reply_text(
            "لا توجد نتائج مؤكدة محفوظة حتى الآن."
        )
        return

    message = "آخر النتائج المؤكدة:\n\n"

    for item in records:
        message += (
            f"Platform: {item['platform']}\n"
            f"Username: {item['username'] or 'Unknown'}\n"
            f"Confidence: {item['confidence']}\n"
            f"Link: {item['live_url'] or 'Unavailable'}\n\n"
        )

    await update.message.reply_text(message)


async def post_init(application: Application):
    initialize()
    logger.info("SalemSniper initialized successfully")


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    if not WEBHOOK_URL:
        raise RuntimeError("RENDER_EXTERNAL_URL is missing")

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

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
        webhook_url=f"{WEBHOOK_URL}/telegram",
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
