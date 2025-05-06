from config import BOT_TOKEN, BACKEND_URL
from migrations.migrations import migrations_handler
from utils.utils import setup_logger
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler
from patterns import PATTERN_COMPUTRABAJO, PATTERN_LINKEDIN, PATTERN_UPDATE_DB, PATTERN_SHOW_VACANTES, PATTERN_USER_DECISION, PATTERN_RETURN_MENU
from conversations.conversations import CHOOSING_SCRAPER, CHOOSING_DATA_OR_APPLY, USER_DECISION, start, choose_scraper, choose_data_or_apply, user_decision, cancel
import requests

logger = setup_logger(__name__)
# Main
def main():
    if BACKEND_URL:
        try:
            requests.get(BACKEND_URL)
            print("✅ Backend corriendo...")
        except Exception as e:
            print("Error en main: Revisar logs para más detalles.")
            logger.error(f"Error en main: {e}")
    else:
        migrations_handler()
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
