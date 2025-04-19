from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters, CallbackQueryHandler
)
from scrapers.computrabajo_scraper import handler as computrabajo_handler, bot_apply
from dotenv import load_dotenv
from config import INTEREST_JOBS
from services.job_service import JobService
import os

load_dotenv()

# Estados de la conversación
CHOOSING_SCRAPER, CHOOSING_DATA_OR_APPLY, SHOWING_VACANCY, USER_DECISION = range(4)

# Token de Telegram
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Variables temporales
vacantes = []
current_index = 0

# Inicia el flujo
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💼 Computrabajo", callback_data='computrabajo'),
            InlineKeyboardButton("🔗 LinkedIn", callback_data='linkedin')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Hola Camilo! ¿Dónde quieres buscar vacantes?",
        reply_markup=reply_markup
    )
    return CHOOSING_SCRAPER

# Callback cuando elige scraper
async def choose_scraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    scraper_name = query.data.lower()
    if scraper_name == 'computrabajo':
        keyboard = [
            [
                InlineKeyboardButton("🗂️ Actualizar base de datos", callback_data='update_db'),
                InlineKeyboardButton("📋 Mostrar vacantes", callback_data='show_vacantes')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "¿Qué quieres hacer?",
            reply_markup=reply_markup
        )
        return CHOOSING_DATA_OR_APPLY
    else:
        await query.edit_message_text("Por ahora solo está disponible Computrabajo 👌")
        return CHOOSING_SCRAPER

# Callback cuando elige acción dentro del scraper
async def choose_data_or_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'update_db':
        await query.edit_message_text("Cargando vacantes...")
        computrabajo_handler(INTEREST_JOBS)
        await query.message.reply_text("✅ Vacantes cargadas.")
        return await choose_scraper(update, context)

    elif query.data == 'show_vacantes':
        return await show_next_vacancy(update, context, query=query)

# Muestra la siguiente vacante
async def show_next_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    global vacantes, current_index
    job_service = JobService()

    if not vacantes:
        vacantes = job_service.get_vacancies()
    if current_index >= len(vacantes):
        msg = "✅ No hay más vacantes."
        if query:
            await query.edit_message_text(msg)
        else:
            await update.effective_message.reply_text(msg)
        return ConversationHandler.END

    vacante = vacantes[current_index]
    response = (
        f"📢 Vacante disponible:\n\n"
        f"📌 *{vacante['title']}*\n"
        f"💵 {vacante['salary']}\n"
        f"📃 {vacante['contract_type']}\n"
        f"🕐 {vacante['schedule']}\n"
        f"🌐 {vacante['modality']}\n"
        f"📝 {vacante['description']}\n\n"
        f"🔗 {vacante['url']}"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Aplicar (bot)", callback_data='apply_bot'),
            InlineKeyboardButton("❌ No aplicar", callback_data='reject'),
        ],
        [
            InlineKeyboardButton("✋ Aplicar manualmente", callback_data='apply_manual')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query:
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.effective_message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

    return USER_DECISION

# Recibe decisión del usuario
async def user_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_index
    query = update.callback_query
    await query.answer()

    decision = query.data
    job_service = JobService()
    vacante = vacantes[current_index]
    url = vacante['url']
    job_id = vacante['job_id']

    if decision == 'apply_bot':
        await query.edit_message_text("Aplicando...")
        response = bot_apply(url, job_id)
        await query.message.reply_text(response[0])
        if not response[1]:
            keyboard = [
                [
                    InlineKeyboardButton("✅ Aplicar (bot)", callback_data='apply_bot'),
                    InlineKeyboardButton("❌ No aplicar", callback_data='reject'),
                ],
                [
                    InlineKeyboardButton("✋ Aplicar manualmente", callback_data='apply_manual')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("Selecciona una opción:", reply_markup=reply_markup)
            return USER_DECISION

    elif decision == 'reject':
        job_service.apply_job('rejected', job_id)
        await query.edit_message_text("❌ Vacante rechazada.")

    elif decision == 'apply_manual':
        job_service.apply_job('applied_manually', job_id)
        await query.edit_message_text("✅ Marcado como aplicada manualmente.")

    current_index += 1
    return await show_next_vacancy(update, context)

# Cancela conversación
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚪 Cancelado.")
    return ConversationHandler.END

# Main del bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    entrys_points = [CommandHandler("start", start)]

    conv_handler = ConversationHandler(
        entry_points=entrys_points,
        states={
            CHOOSING_SCRAPER: [CallbackQueryHandler(choose_scraper, pattern="^(computrabajo|linkedin)$")],
            CHOOSING_DATA_OR_APPLY: [CallbackQueryHandler(choose_data_or_apply, pattern="^(update_db|show_vacantes)$")],
            USER_DECISION: [CallbackQueryHandler(user_decision, pattern="^(apply_bot|reject|apply_manual)$")],
        },
        fallbacks=[CommandHandler("cancelar", cancel)]
    )

    app.add_handler(conv_handler)

    print("✅ Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
