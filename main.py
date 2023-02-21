import logging
import sqlite3
from uuid import uuid4
import os

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import Data_file

from BDconnect import BDconnect
from ResponseManager import ResponseManager

import Dictionary

bdConnect = BDconnect()
TokenBot = Data_file.Token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


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
    print(Dictionary.UserState.values())"""
    
    
    application = ApplicationBuilder().token(TokenBot).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
