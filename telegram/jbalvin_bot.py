from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from escritor import complete_text
from dotenv import load_dotenv
import os

load_dotenv()
token=os.getenv("token")

INPUT_TEXT = 0


def start(update, context):

    update.message.reply_text(
        text='Hola, bienvenido, qué te gustaría revisar?\n\nSi ya has escrito una canción recuerda que puedes usar el comando /start para volver a este menú',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Quiero escribir una canción', callback_data='escribe')],
            [InlineKeyboardButton(text='¿Cómo funciona?', callback_data="funciona")],
            [InlineKeyboardButton(text='Quiero ver el github', url='https://github.com/Ojedalatronico/Reggaeton_songs')],
        ])
    )


def escribe_callback_handler(update, context):

    query = update.callback_query
    query.answer()

    query.message.reply_text(
        text='¿Con qué palabras quieres que comience tu canción?'
    )

    return INPUT_TEXT

def funciona(update, context):

    query = update.callback_query
    query.answer()

    query.message.reply_text(
        text='Cuando escribes qué palabras quieres en una canción, un modelo entrenado con natural-language-processing, una red neuronal, realiza una predicción de qué debería continuar a partir de unas canciones con las que fue entrenado anteriormente'
    )

    return ConversationHandler.END


def input_text(update, context):
    text = update.message.text
    chat = update.message.chat
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    update.message.reply_text(complete_text(text))
    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern='escribe', callback=escribe_callback_handler),
            CallbackQueryHandler(pattern='funciona', callback=funciona)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },
        fallbacks=[]
    ))
    updater.start_polling()
    updater.idle()