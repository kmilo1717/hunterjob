from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
)
from scrapers.computrabajo_scraper import handler as computrabajo_handler
from config import BOT_TOKEN

# Estados de la conversación
CHOOSING_SCRAPER, SHOWING_VACANCY, USER_DECISION = range(3)

# Variable temporal
vacantes = []
current_index = 0

# Inicia el flujo
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola Camilo! ¿Dónde quieres buscar vacantes?\n 1. Computrabajo\n 2. LinkedIn")
    vacantes = computrabajo_handler("python")
    return CHOOSING_SCRAPER

# Selecciona scraper
async def choose_scraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global vacantes, current_index
    scraper_name = update.message.text.lower()

    if scraper_name == '1':
        vacantes = computrabajo_handler("python")
        current_index = 0
        if not vacantes:
            update.message.reply_text("No encontré vacantes 😞")
            return ConversationHandler.END
        show_next_vacancy(update, context)
        return USER_DECISION
    else:
        update.message.reply_text("Opción no válida. Escribe 'computrabajo' por ahora.")
        return CHOOSING_SCRAPER

# Muestra la siguiente vacante
async def show_next_vacancy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global vacantes, current_index

    if current_index >= len(vacantes):
        await update.message.reply_text("✅ No hay más vacantes.")
        return ConversationHandler.END

    vacante = vacantes[current_index]
    response = f"Vacante:\n📌 {vacante['title']}\n🔗 {vacante['link']}\n\n¿Quieres aplicar? (sí / no)"
    await update.message.reply_text(response)

# Recibe decisión del usuario
async def user_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_index

    decision = update.message.text.lower()

    if decision == 'sí':
        # Aquí puedes llamar a Selenium para aplicar
        await update.message.reply_text("✅ Aplicado (ficticio por ahora).")
        # También podrías guardar en BD
    elif decision == 'no':
        await update.message.reply_text("❌ Ok, no aplicada.")
    else:
        await update.message.reply_text("Responde 'sí' o 'no'.")
        return USER_DECISION

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
            CHOOSING_SCRAPER: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_scraper)],
            USER_DECISION: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_decision)]
        },
        fallbacks=[CommandHandler("cancelar", cancel)]
    )

    app.add_handler(conv_handler)

    print("✅ Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
