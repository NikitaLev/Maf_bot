import asyncio
import logging
import sqlite3
from uuid import uuid4
import os

import telegram
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import Data_file

from BDconnect import BDconnect
from ResponseManager import ResponseManager
from SendingMessagesManager import SendingMessagesManager

import Dictionary

bdConnect = BDconnect()
TokenBot = Data_file.Token
#bot = telegram.Bot(TokenBot)

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
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    response = responseManager.generate_response_with_name()

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)

async def sending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sendingMessagesManager = SendingMessagesManager()
    list_user_for_sending = sendingMessagesManager.user_sending

    for user in list_user_for_sending:
        name = user[0]
        id = user[1]
        template = sendingMessagesManager.get_template_sending_with_name() % name
        await context.bot.send_message(chat_id=id,
                                            text=template)


    #response = responseManager.generate_response_with_name()

    #await context.bot.send_message(chat_id=update.effective_chat.id,
    #                               text=response)

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('img_test')
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    response = responseManager.generate_response_with_name()

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)
    """print(3)
    print(context._user_id)
    key = str(uuid4())
    for r in context.user_data:
        print(r, "user_data")
    if key in context.user_data:
        print(key, context.user_data[key])
    else:
        print(key, ' text empty')
        context.user_data[key] = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)"""


async def put(update, context):
    """Usage: /put value"""
    # Generate ID and separate value from command
    print(1)
    key = str(uuid4())
    print('key ', key)
    # We don't use context.args here, because the value may contain whitespaces

    print('update.message.text ', update.message.text)
    value = update.message.text.partition(' ')[2]
    print('value ', value)

    # Store value
    context.user_data[key] = value
    # Send the key to the user
    await update.message.reply_text(key)


#'👍😅🙃😂😘❤️😍😊😁'
#👍😅🙃😂😘❤️😍😊😁

async def get(update, context):
    print(2)
    """Usage: /get uuid"""
    # Separate ID from command
    key = context.args[0]
    print('key ', key)

    # Load value and send it to the user
    value = context.user_data.get(key, 'Not found')
    print('value ', value)
    await update.message.reply_text(value)


if __name__ == '__main__':
    """print(Dictionary.response_template_in_state)
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
    bdConnect.insert_user(name='tttt', user_id=11111, mafia_name="test")
"""

    application = ApplicationBuilder().token(TokenBot).build()

    start_handler = CommandHandler('start', start)
    sending_handler = CommandHandler('sending', sending)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND), photo)

    application.add_handler(start_handler)
    application.add_handler(sending_handler)

    application.add_handler(echo_handler)
    application.add_handler(photo_handler)

    application.run_polling()