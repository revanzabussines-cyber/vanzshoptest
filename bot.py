import os
import logging
from datetime import datetime

from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

# ==========================
# LOGGING
# ==========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==========================
# CONFIG
# ==========================

# Ambil token dari Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum di-set. Tambahin di Environment Render dulu.")


# ==========================
# HANDLER COMMAND
# ==========================

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    text = (
        f"👋 Halo, *{user.first_name or 'Kak'}!*\n\n"
        "Ini bot sample VanzShop, siap lu modif jadi apa aja.\n\n"
        "Perintah yang tersedia:\n"
        "• /start – buka menu awal\n"
        "• /help – bantuan & info bot\n"
        "• /ping – cek bot hidup apa nggak\n"
        "• Kirim teks biasa → bot akan reply mirroring\n"
    )
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def help_cmd(update: Update, context: CallbackContext):
    text = (
        "🛠 *Bantuan VanzShop Bot*\n\n"
        "Bot ini cuma kerangka dasar yang bisa lu kembangin sendiri.\n\n"
        "Contoh ide fitur:\n"
        "• Auto-order / cek status pesanan\n"
        "• Generate ID Card / kartu member\n"
        "• Broadcast info restock ke user\n\n"
        "Source code sudah siap buat di-deploy di Render.\n"
    )
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def ping(update: Update, context: CallbackContext):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    update.message.reply_text(f"🏓 *PONG!*\nBot aktif.\nUTC time: `{now}`", parse_mode=ParseMode.MARKDOWN)


# ==========================
# HANDLER TEXT BIASA
# ==========================

def echo_text(update: Update, context: CallbackContext):
    msg = update.message.text

    # contoh logic simple: kalau ada kata 'order'
    if "order" in msg.lower():
        reply = (
            "🛒 Kayaknya kak lagi ngomongin *order* nih.\n"
            "Ini cuma contoh respon. Nanti bisa lu ganti jadi alur auto order asli. 😉"
        )
    else:
        reply = f"Lu bilang:\n`{msg}`\n\n(ini cuma echo, silakan modif jadi fitur lain)"
    update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


# ==========================
# MAIN
# ==========================

def main():
    logger.info("Mulai jalanin bot...")

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("ping", ping))

    # Text biasa
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_text))

    # Start bot
    updater.start_polling()
    logger.info("Bot sudah online dan polling update Telegram...")
    updater.idle()


if __name__ == "__main__":
    main()
