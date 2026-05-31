import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

BOT_TOKEN = "8633461710:AAFsuZnkRhTwcVbPVJcUfHUNU5baRad36Ns"
ADMIN_ID = "denizesk26"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👊 Welcome to Slap Bibi!\n\n"
        "🇵🇸 Every slap feeds Gaza.\n\n"
        "$SLAPBIBI is a Solana meme coin — 25% of all trading fees "
        "go directly to the World Food Programme Gaza emergency fund.\n\n"
        "🌐 slapbibi.fun\n"
        "💬 t.me/SlapBibiCommunity\n\n"
        "━━━━━━━━━━━━━━━\n"
        "📩 Have a question or want to get in touch?\n"
        "Just send your message below and our team will get back to you!\n\n"
        "🇵🇸 Free Palestine"
    )

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    user_id = user.id
    username = f"@{user.username}" if user.username else user.first_name
    admin_text = (
        f"📩 New message:\n"
        f"From: {username} (ID: {user_id})\n"
        f"Name: {user.first_name}\n\n"
        f"Message:\n{message}\n\n"
        f"To reply: /reply {user_id} your message here"
    )
    try:
        await context.bot.send_message(chat_id=f"@{ADMIN_ID}", text=admin_text)
    except Exception as e:
        logger.error(f"Admin mesaj hatası: {e}")
    await update.message.reply_text(
        "✅ Your message has been received!\n\n"
        "Our team will get back to you as soon as possible.\n\n"
        "🇵🇸 Free Palestine | slapbibi.fun"
    )

async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_ID.replace("@", ""):
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply USER_ID message text")
        return
    try:
        target_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(
            chat_id=target_id,
            text=f"💬 Reply from Slap Bibi team:\n\n{reply_text}\n\n🇵🇸 slapbibi.fun"
        )
        await update.message.reply_text("✅ Reply sent!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    logger.info("Bot starting...")
    async with app:
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
