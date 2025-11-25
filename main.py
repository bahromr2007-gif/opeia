import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import openai

# ================== API KALITNI ULASH ==================
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# ================== LOG ==================
logging.basicConfig(level=logging.INFO)

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Referat yaratish", callback_data="referat_menu")]
    ]
    await update.message.reply_text(
        "Assalomu alaykum!\nQuyidagi tugma orqali referat turini tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== MENYU ==================
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "referat_menu":
        keyboard = [
            [InlineKeyboardButton("📄 Oddiy referat", callback_data="oddiy")],
            [InlineKeyboardButton("📘 Katta referat", callback_data="katta")],
            [InlineKeyboardButton("📑 Reja bilan referat", callback_data="reja")],
        ]
        await query.edit_message_text(
            "Referat turini tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data in ["oddiy", "katta", "reja"]:
        context.user_data["referat_turi"] = query.data
        await query.edit_message_text("Mavzuni yuboring:")

# ================== REFERAT YARATISH ==================
async def generate_referat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mavzu = update.message.text
    turi = context.user_data.get("referat_turi", "oddiy")

    await update.message.reply_text("⏳ Referat tayyorlanmoqda, kuting...")

    # Prompt tayyorlash
    if turi == "oddiy":
        prompt = f"'{mavzu}' mavzusida 1.5–2 sahifalik sodda referat yoz."
    elif turi == "katta":
        prompt = f"'{mavzu}' mavzusida 3–5 sahifalik batafsil katta referat yoz."
    elif turi == "reja":
        prompt = f"'{mavzu}' mavzusi bo‘yicha reja bilan 2–3 sahifalik referat yoz."

    # OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    matn = response.choices[0].message["content"]

    await update.message.reply_text(matn)

# ================== ASOSIY ==================
def main():
    BOT_TOKEN = "8160297478:AAGMPl-SMEzTEAzfwXK_ZnaAQ_C9MX61fK0"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_referat))

    app.run_polling()

if __name__ == "__main__":
    main()
