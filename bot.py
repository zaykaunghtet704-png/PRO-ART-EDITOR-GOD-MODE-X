"""Telegram bot worker. Editing features are added in later milestones."""
from __future__ import annotations

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from config import APP_NAME, BOT_TOKEN, OWNER_ID

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("god-mode-x")


def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🖼️ Photo Studio", callback_data="menu:photo"),
         InlineKeyboardButton("🎬 Video Studio", callback_data="menu:video")],
        [InlineKeyboardButton("✨ AI Art & Logo", callback_data="menu:art"),
         InlineKeyboardButton("👤 My Account", callback_data="menu:account")],
        [InlineKeyboardButton("❓ Help", callback_data="menu:help")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = (
        f"🔥 {APP_NAME}\n\n"
        "Photo, Video, Logo နဲ့ AI Creative Studio ကို တစ်နေရာတည်းမှာ "
        "အသုံးပြုနိုင်မယ့် Platform ဖြစ်ပါတယ်။\n\n"
        "စတင်တည်ဆောက်နေဆဲဖြစ်ပြီး လုပ်ဆောင်ချက်တွေကို အဆင့်လိုက် ဖွင့်ပေးသွားပါမယ်။"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu())


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    section = (query.data or "").split(":", 1)[-1]
    messages = {
        "photo": "🖼️ Photo Studio\nBatch editing, enhancement နဲ့ background tools များကို နောက်အဆင့်တွင် ချိတ်ဆက်ပါမယ်။",
        "video": "🎬 Video Studio\nMP4 / MOV export နဲ့ video processing engine ကို နောက်အဆင့်တွင် ချိတ်ဆက်ပါမယ်။",
        "art": "✨ AI Art & Logo\nAI image generation နဲ့ logo tools များကို API ချိတ်ဆက်ပြီး ဖွင့်ပါမယ်။",
        "account": "👤 Account\nသင့် Telegram ID: " + str(query.from_user.id),
        "help": "❓ Help\n/start — Main menu\n/id — Telegram ID\nလက်ရှိ Version: 0.1.0 (Foundation)",
    }
    await query.edit_message_text(
        messages.get(section, "မသိသော Menu ဖြစ်ပါတယ်။"),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ Main Menu", callback_data="menu:home")]]
        ),
    )
    if section == "home":
        await query.edit_message_text(
            f"🔥 {APP_NAME}\nMain Menu",
            reply_markup=main_menu(),
        )


async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.message:
        await update.message.reply_text(f"Your Telegram ID: {update.effective_user.id}")


async def owner_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or update.effective_user.id != OWNER_ID:
        if update.message:
            await update.message.reply_text("ဒီ Command ကို Bot Owner သာ အသုံးပြုနိုင်ပါတယ်။")
        return
    if update.message:
        await update.message.reply_text(
            f"👑 Owner Panel\nBot: {APP_NAME}\nVersion: 0.1.0\nStatus: Foundation"
        )


def run() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Add it in Render Environment.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("id", user_id))
    app.add_handler(CommandHandler("owner", owner_status))
    app.add_handler(CallbackQueryHandler(menu_callback, pattern=r"^menu:"))
    logger.info("Starting %s Telegram worker", APP_NAME)
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    run()
