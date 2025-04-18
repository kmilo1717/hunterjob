from telegram import Bot
from telegram.ext import Updater, CommandHandler
import sqlite3

# Usa tu token de Telegram aquí
TOKEN = 'TU_TOKEN_DE_BOT'

def start(update, context):
    update.message.reply_text("¡Hola! Estoy buscando vacantes para ti. Usa /vacantes para verlas.")

def vacantes(update, context):
    conn = sqlite3.connect('vacantes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM vacantes LIMIT 5')  # Limitar a las 5 primeras vacantes
    vacantes = c.fetchall()
    
    response = "Vacantes disponibles:\n\n"
    for vacante in vacantes:
        response += f"{vacante[1]}\n{vacante[2]}\n{vacante[4]}\n\n"  # Muestra solo título, empresa y enlace
    
    update.message.reply_text(response)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("vacantes", vacantes))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
