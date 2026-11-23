"""Telegram interface for PRO ART EDITOR GOD MODE X."""
from __future__ import annotations
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)
from config import APP_NAME, BOT_TOKEN, OWNER_ID

logger = logging.getLogger("god-mode-x.bot")
DIVIDER = "━━━━━━━━━━━━━━━━━━━━"

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼️  PHOTO STUDIO", callback_data="page:photo"),
         InlineKeyboardButton("🎬  VIDEO STUDIO", callback_data="page:video")],
        [InlineKeyboardButton("✨  AI ART & LOGO", callback_data="page:art"),
         InlineKeyboardButton("🎧  AUDIO LAB", callback_data="page:audio")],
        [InlineKeyboardButton("👤  MY ACCOUNT", callback_data="page:account"),
         InlineKeyboardButton("📚  HELP CENTER", callback_data="page:help")],
        [InlineKeyboardButton("⚙️  SYSTEM STATUS", callback_data="page:status")],
    ])

def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(
        "⬅️  BACK TO MAIN MENU", callback_data="page:home")]])

def welcome_text(user_name: str) -> str:
    return (
        "✦ 𝗣𝗥𝗢 𝗔𝗥𝗧 𝗘𝗗𝗜𝗧𝗢𝗥 ✦\n"
        "╭━━━━━━━━━━━━━━━━━━━━╮\n"
        "     𝗚𝗢𝗗 𝗠𝗢𝗗𝗘 𝗫  •  𝗩𝟬.𝟮\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
        f"မင်္ဂလာပါ {user_name} 👋\n"
        "သင့်ရဲ့ Creative Studio မှ ကြိုဆိုပါတယ်။\n\n"
        "🖼️ Photo  •  🎬 Video\n✨ AI Art  •  🎨 Logo  •  🎧 Audio\n\n"
        "အောက်က Menu ကိုရွေးချယ်ပြီး ဆက်သွားပါ။\n"
        f"{DIVIDER}\n⚡ Quality • Creativity • Innovation"
    )

PAGES = {
    "photo": ("🖼️ 𝗣𝗛𝗢𝗧𝗢 𝗦𝗧𝗨𝗗𝗜𝗢\n" + DIVIDER +
              "\n• Image Enhancement / Sharpen\n• Background Remove / Replace"
              "\n• Object Remove / Retouch\n• Color Grade / Restoration"
              "\n• Batch Photo Editing\n\n🔒 Photo engine မချိတ်ဆက်ရသေးပါ။"),
    "video": ("🎬 𝗩𝗜𝗗𝗘𝗢 𝗦𝗧𝗨𝗗𝗜𝗢\n" + DIVIDER +
              "\n• Cut / Merge / Compress\n• Subtitles / Audio / Transitions"
              "\n• Stabilization / Slow Motion\n• MP4 + MOV export"
              "\n• 4K output (server/source ပေါ်မူတည်)"
              "\n\n🔒 Video engine မချိတ်ဆက်ရသေးပါ။"),
    "art": ("✨ 𝗔𝗜 𝗔𝗥𝗧 & 𝗟𝗢𝗚𝗢\n" + DIVIDER +
            "\n• AI Image Generation\n• 3D / Gaming / Business Logo"
            "\n• Poster / Banner / Thumbnail\n• Sticker / Brand Kit / Cover"
            "\n\n🔒 AI Provider API မချိတ်ဆက်ရသေးပါ။"),
    "audio": ("🎧 𝗔𝗨𝗗𝗜𝗢 𝗟𝗔𝗕\n" + DIVIDER +
              "\n• Noise Reduction / Voice Clean\n• Audio Trim / Convert"
              "\n• MP3 Extraction / Equalizer"
              "\n\n🔒 Audio engine မချိတ်ဆက်ရသေးပါ။"),
    "help": ("📚 𝗛𝗘𝗟𝗣 𝗖𝗘𝗡𝗧𝗘𝗥\n" + DIVIDER +
             "\n/start — Main Menu\n/help — Help Center\n/id — Telegram ID"
             "\n/status — Bot Status\n/owner — Owner Panel"
             "\n\nVersion: 0.2.0\nပြဿနာရှိပါက Bot Owner ကို ဆက်သွယ်ပါ။"),
    "status": ("⚙️ 𝗦𝗬𝗦𝗧𝗘𝗠 𝗦𝗧𝗔𝗧𝗨𝗦\n" + DIVIDER +
               "\n🌐 API: Running\n🤖 Telegram: Running"
               "\n🖼️ Photo engine: Not connected\n🎬 Video engine: Not connected"
               "\n✨ AI provider: Not connected\n🎧 Audio engine: Not connected"
               "\n\nMenu အလုပ်လုပ်ခြင်းနှင့် Editing Engine အလုပ်လုပ်ခြင်း မတူပါ။"),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        user = update.effective_user
        await update.effective_message.reply_text(
            welcome_text(user.first_name if user else "Creator"),
            reply_markup=main_menu())

async def show_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    page = (query.data or "").split(":", 1)[-1]
    if page == "home":
        await query.edit_message_text(welcome_text(query.from_user.first_name),
                                       reply_markup=main_menu())
        return
    if page == "account":
        user = query.from_user
        content = ("👤 𝗠𝗬 𝗔𝗖𝗖𝗢𝗨𝗡𝗧\n" + DIVIDER +
                   f"\nName: {user.full_name}\nUser ID: {user.id}"
                   f"\nUsername: @{user.username or 'မရှိပါ'}"
                   "\nPlan: Free\nCredits: 0")
    else:
        content = PAGES.get(page, "ဒီ Menu ကို ရှာမတွေ့ပါ။")
    await query.edit_message_text(content, reply_markup=back_menu())

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message and update.effective_user:
        await update.effective_message.reply_text(
            f"🆔 Your Telegram ID: {update.effective_user.id}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(PAGES["status"])

async def owner_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or user.id != OWNER_ID:
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ ဒီ Command ကို Bot Owner သာ အသုံးပြုနိုင်ပါတယ်။")
        return
    if update.effective_message:
        await update.effective_message.reply_text(
            "👑 𝗢𝗪𝗡𝗘𝗥 𝗖𝗢𝗡𝗧𝗥𝗢𝗟\n" + DIVIDER +
            f"\nBot: {APP_NAME}\nVersion: 0.2.0\nStatus: Online"
            "\nEditing engines: Pending integration")

async def unsupported_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "📥 ဖိုင်လက်ခံရရှိပါတယ်။\n"
            "လက်ရှိမှာ Editing Engine မချိတ်ဆက်ရသေးလို့ ဖိုင်ကို မပြုပြင်နိုင်သေးပါ။")

async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "မင်္ဂလာပါ 👋 Menu ဖွင့်ရန် /start ကိုနှိပ်ပါ။")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled Telegram update error: %s", context.error,
                 exc_info=context.error)

def build_application() -> Application:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Add it in Render Environment.")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("id", user_id))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("owner", owner_status))
    application.add_handler(CallbackQueryHandler(show_page, pattern=r"^page:"))
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.Document.ALL, unsupported_media))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, unknown_text))
    application.add_error_handler(error_handler)
    return application

def main() -> None:
    build_application().run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
