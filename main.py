import asyncio
import logging
import sqlite3
from uuid import uuid4
import os

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, CallbackQueryHandler, ApplicationBuilder, CommandHandler, ContextTypes
import Data_file

from BDconnect import BDconnect
from ResponseManager import ResponseManager
from SendingMessagesManager import SendingMessagesManager

import Dictionary

bdConnect = BDconnect()
TokenBot = Data_file.Token
# bot = telegram.Bot(TokenBot)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

"""async def test():
    await bot.send_message(chat_id=490466369, text='test')"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bdConnect.insert_user(name=update.effective_user.full_name, user_id=update.effective_user.id, mafia_name="-")

    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    response = responseManager.generate_response_no_name()
    responseManager.set_user_state(2)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('echo', update.message.text)
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    response = responseManager.generate_response_with_name()

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)


async def sending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    if bdConnect.get_user_level(user_id=responseManager.user_id):
        sendingMessagesManager = SendingMessagesManager()
        list_user_for_sending = sendingMessagesManager.user_sending

        for user in list_user_for_sending:
            responseMan = ResponseManager(user_id=user[1], message=update.message.text)
            responseMan.response_to_invitation_question()

            template = sendingMessagesManager.get_template_sending_with_name() % responseMan.user_name_mf
            #await context.bot.send_message(chat_id=id,text=template)

            keyboard = [
                [InlineKeyboardButton("Приду на игры", callback_data='+')],
                [InlineKeyboardButton("В следующий раз", callback_data='-')],
                [InlineKeyboardButton("Пока не знаю", callback_data='?')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=responseMan.user_id, text=template, reply_markup=reply_markup)

        response = responseManager.generate_response_for_super_user_sending(name=responseManager.user_name_mf)

        await context.bot.send_message(chat_id=responseManager.user_id,
                                       text=response)
    else:
        response = responseManager.generate_response_for_default_user_sending(name=responseManager.user_name_mf)
        await context.bot.send_message(chat_id=responseManager.user_id,
                                       text=response)


async def response_to_invitation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    variant = query.data
    print('query', query)
    print('variant', variant)
    print('variant', query.message)
    template = ''

    responseManager = ResponseManager(user_id=update.effective_user.id, message=variant)
    if variant == '+':
        template = responseManager.response_to_invitation_true()
    elif variant == '-':
        template = responseManager.response_to_invitation_false()
    else:
        template = responseManager.response_to_invitation_question()
    await context.bot.send_message(chat_id=responseManager.user_id, text=template)
"""    await query.answer()
    await query.edit_message_text(text=f"Выбранный вариант: {variant}")
    keyboard = [
        [InlineKeyboardButton("Приду на игры", callback_data='test')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)"""


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('img_test')
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    response = responseManager.generate_response_with_name()

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)
# '👍😅🙃😂😘❤️😍😊😁'
# 👍😅🙃😂😘❤️😍😊😁


def test_mod():
    bdConnect.set_super_user_level(490466369)
    """
    print(Dictionary.response_template_in_state)
    print(Dictionary.response_template_in_state.get(0))
    print(Dictionary.UserState)
    print(Dictionary.UserState.get(list(Dictionary.UserState.keys())[0]))
    test_string ='test name: %s'
    names = 'name'
    test2_string = test_string % names
    print(test_string)
    print(test2_string)
    for r in Dictionary.UserState.keys():
        print(r)
    print(list(Dictionary.UserState.keys())[0])
    print(Dictionary.UserState.values())


    bdConnect.update_user_state_sending(user_id=11111, state_sending=False)
    sendingMessagesManager = SendingMessagesManager()

    test = test()
    asyncio.run(test)
    bdConnect.insert_user(name='tttt', user_id=11111, mafia_name="test")    490466369
"""


if __name__ == '__main__':

    test_mod()

    application = ApplicationBuilder().token(TokenBot).build()

    start_handler = CommandHandler('start', start)
    sending_handler = CommandHandler('sending', sending)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND), photo)

    application.add_handler(CallbackQueryHandler(response_to_invitation))

    application.add_handler(start_handler)
    application.add_handler(sending_handler)

    application.add_handler(echo_handler)
    application.add_handler(photo_handler)

    application.run_polling()
