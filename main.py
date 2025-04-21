# -*- coding: utf-8 -*-
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ConversationHandler, ContextTypes,
    CallbackQueryHandler
)
from scrapers.computrabajo_scraper import handler as computrabajo_handler, bot_apply
from config import INTEREST_JOBS, BOT_TOKEN
from services.job_service import JobService
from utils.utils import setup_logger, highlights
import html

logger = setup_logger(__name__)

# Estados
CHOOSING_SCRAPER, CHOOSING_DATA_OR_APPLY, USER_DECISION = range(3)

# Patrones
PATTERN_COMPUTRABAJO = "computrabajo"
PATTERN_LINKEDIN = "linkedin"
PATTERN_UPDATE_DB = "update_db"
PATTERN_SHOW_VACANTES = "show_vacantes"
PATTERN_USER_DECISION = "^(apply_bot|reject|apply_manual)$"
PATTERN_RETURN_MENU = "return_menu"

# Comienza conversación
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💼 Computrabajo", callback_data=PATTERN_COMPUTRABAJO),
         InlineKeyboardButton("🔗 LinkedIn", callback_data=PATTERN_LINKEDIN)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Hola Camilo! ¿Dónde quieres buscar vacantes?", reply_markup=reply_markup)
    return CHOOSING_SCRAPER

# Elige scraper
async def choose_scraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        scraper_name = query.data.lower()
        if scraper_name == PATTERN_COMPUTRABAJO:
            keyboard = [
                [InlineKeyboardButton("🗂️ Actualizar base de datos", callback_data=PATTERN_UPDATE_DB),
                InlineKeyboardButton("📋 Mostrar vacantes", callback_data=PATTERN_SHOW_VACANTES)],
                [InlineKeyboardButton("🔙 Volver al menú", callback_data=PATTERN_RETURN_MENU)]
            ]
            await query.edit_message_text("¿Qué quieres hacer?", reply_markup=InlineKeyboardMarkup(keyboard))
            return CHOOSING_DATA_OR_APPLY
        else:
            await query.edit_message_text("Por ahora solo está disponible Computrabajo 👌")
            return CHOOSING_SCRAPER

    except Exception as e:
        print("Error en choose_scraper: Revisar logs para más detalles.")
        logger.error(f"Error en choose_scraper: {e}")

# Acciones del scraper
async def choose_data_or_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == PATTERN_UPDATE_DB:
            await query.edit_message_text("Cargando vacantes...")
            computrabajo_handler(INTEREST_JOBS)
            await query.message.reply_text("✅ Vacantes cargadas.")
            return await choose_scraper(update, context)

        elif query.data == PATTERN_SHOW_VACANTES:
            context.user_data['vacantes'] = JobService().get_vacancies()
            context.user_data['current_index'] = 0
            return await show_next_vacancy(update, context, query=query)

        elif query.data == PATTERN_RETURN_MENU:
            return await start(update, context)

    except Exception as e:
        print("Error en choose_data_or_apply: Revisar logs para más detalles.")
        logger.error(f"Error en choose_data_or_apply: {e}")

# Muestra vacante
async def show_next_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    try:
        vacantes = context.user_data.get('vacantes', [])
        current_index = context.user_data.get('current_index', 0)

        if not vacantes or current_index >= len(vacantes):
            msg = "✅ No hay más vacantes."
            if query:
                await query.edit_message_text(msg)
            else:
                await update.effective_message.reply_text(msg)
            return ConversationHandler.END

        vacante = dict(vacantes[current_index])
        response = ""
        
        if 'url' in vacante and vacante['url']:
            response += f"🔗 {vacante['url']}\n"
        if 'description' in vacante and vacante['description']:
            desc = vacante['description']
            if len(desc) > 3500:
                desc = desc[:3500] + '...'
            response += f"📝 {desc}\n\n"
        if 'title' in vacante and vacante['title']:
            response += f"📌 <b>{vacante['title']}</b>\n"
        if 'company' in vacante and vacante['company']:
            response += f"🏢 <b>{vacante['company']}</b>\n"
        if 'modality' in vacante and vacante['modality']:
            response += f"⚠️ <b>{vacante['modality']}</b>\n"
        if 'location' in vacante and vacante['location']:
            response += f"📍 <b>{vacante['location']}</b>\n"
        if 'salary' in vacante and vacante['salary']:
            response += f"💵 {vacante['salary']}\n"
        if 'contract_type' in vacante and vacante['contract_type']:
            response += f"📃 {vacante['contract_type']}\n"
        if 'schedule' in vacante and vacante['schedule']:
            response += f"🕐 {vacante['schedule']}\n"

        response = highlights(response)

        keyboard = [
            [InlineKeyboardButton("✅ Aplicar (bot)", callback_data='apply_bot'),
            InlineKeyboardButton("❌ No aplicar", callback_data='reject')],
            [InlineKeyboardButton("✋ Aplicar manualmente", callback_data='apply_manual')]
        ]

        try:
            if query:
                await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML", disable_web_page_preview=True)
            else:
                await update.effective_message.reply_text(response, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            logger.error(f"Error al mostrar formato HTML: {e}")
            safe_response = html.escape(response)
            if query:
                await query.edit_message_text(safe_response, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
            else:
                await update.effective_message.reply_text(safe_response, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

        return USER_DECISION

    except Exception as e:
        print("Error al mostrar la vacante: Revisar logs para más detalles.")
        logger.error(f"Error al mostrar la vacante: {e}")

# Decisión del usuario
async def user_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        decision = query.data
        job_service = JobService()
        vacantes = context.user_data.get('vacantes', [])
        current_index = context.user_data.get('current_index', 0)
        vacante = vacantes[current_index]
        job_id = vacante['job_id']
        url = vacante['url']

        if decision == 'apply_bot':
            await query.edit_message_text("Aplicando...")
            response = bot_apply(url, job_id)
            await query.message.reply_text(response[0])
            if response[1]:
                context.user_data['current_index'] += 1
            else:
                await query.message.reply_text("No se pudo aplicar automáticamente.")

        elif decision == 'reject':
            job_service.apply_job('rejected', job_id)
            await query.edit_message_text("❌ Vacante rechazada.")
            context.user_data['current_index'] += 1

        elif decision == 'apply_manual':
            job_service.apply_job('applied_manually', job_id)
            await query.edit_message_text("✅ Marcado como aplicada manualmente.")
            context.user_data['current_index'] += 1

        return await show_next_vacancy(update, context)

    except Exception as e:
        print("Error en user_decision: Revisar logs para más detalles.")
        logger.error(f"Error en user_decision: {e}")

# Cancela
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚪 Cancelado.")
    return ConversationHandler.END

# Main
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_SCRAPER: [CallbackQueryHandler(choose_scraper, pattern=f"^({PATTERN_COMPUTRABAJO}|{PATTERN_LINKEDIN})$")],
            CHOOSING_DATA_OR_APPLY: [CallbackQueryHandler(choose_data_or_apply, pattern=f"^({PATTERN_UPDATE_DB}|{PATTERN_SHOW_VACANTES}|{PATTERN_RETURN_MENU})$")],
            USER_DECISION: [CallbackQueryHandler(user_decision, pattern=PATTERN_USER_DECISION)]
        },
        fallbacks=[CommandHandler("cancelar", cancel)]
    )

    app.add_handler(conv_handler)
    print("✅ Bot corriendo...")
    logger.info("Bot corriendo con exito.")
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error en main: Revisar logs para más detalles.")
        logger.error(f"Error en main: {e}")
