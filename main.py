import asyncio
import logging
import sqlite3
from uuid import uuid4
import os

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, CallbackQueryHandler, ApplicationBuilder, CommandHandler, ContextTypes
import Data_file
import base64

from fuzzywuzzy import fuzz
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
    print('echo ', update.message.text)
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    if responseManager.super_user:
        if responseManager.user_state == 4:  # ожидание текста поста
            response = responseManager.add_text_in_post()
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=response)
            # bdConnect.add_text_in_post(responseManager.message, responseManager.user_post)
        elif responseManager.user_state == 5:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Требуется фото')
        elif responseManager.user_state == 6:

            text_data = ''
            photo_data = ''

            if responseManager.message.isdigit():
                text_data, photo_data = post_creator(bdConnect.get_post(responseManager.message))
                responseManager.set_user_state(7)
            else:
                recognize_result = recognize_cmd(responseManager.message)
                if (recognize_result['cmd'] == "sending_command" or recognize_result['cmd'] == "yes") \
                        and recognize_result['percent'] > 50:
                    text_data, photo_data = post_creator(responseManager.get_data_post_user())
                    responseManager.set_user_state(7)
                elif (recognize_result['cmd'] == "not" or recognize_result['cmd'] == "deactivation_post") \
                        and recognize_result['percent'] > 50:
                    response = responseManager.deactivation_post_user()
                    await context.bot.send_message(chat_id=responseManager.user_id,
                                                   text=response)
                else:
                    response = responseManager.not_recognized_text()
                    await context.bot.send_message(chat_id=responseManager.user_id,
                                                   text=response)
                    return 0

            sendingMessagesManager = SendingMessagesManager()
            list_user_for_sending = sendingMessagesManager.user_sending
            for user in list_user_for_sending:
                responseMan = ResponseManager(user_id=user[1], message=update.message.text)
                responseMan.response_to_invitation_question()

                template = text_data
                # await context.bot.send_message(chat_id=id,text=template)

                keyboard = [
                    [InlineKeyboardButton("Приду на игры", callback_data='+')],
                    [InlineKeyboardButton("В следующий раз", callback_data='-')],
                    [InlineKeyboardButton("Пока не знаю", callback_data='?')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await context.bot.send_photo(chat_id=update.effective_chat.id,
                                             photo=photo_data)
                await context.bot.send_message(chat_id=responseMan.user_id, text=template, reply_markup=reply_markup)

            response = responseManager.generate_response_for_super_user_sending(name=responseManager.user_name_mf)

            await context.bot.send_message(chat_id=responseManager.user_id,
                                           text=response)
        elif responseManager.user_state == 7:
            recognize_result = recognize_cmd(responseManager.message)
            if recognize_result['cmd'] == "deactivation_post"\
                    and recognize_result['percent'] > 50:
                response = responseManager.generate_response_no_name()
                responseManager.deactivation_post_user()
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=response)
    else:
        response = responseManager.generate_response_with_name()

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=response)


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in Dictionary.VA_CMD_LIST.items():
        for x in v:
            # print('rc', rc)
            vrt = fuzz.ratio(cmd, x)
            # print(x + ' x = '+str(vrt))
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc


def post_creator(data):
    if data:
        return data[3], data[4]


async def sending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    if responseManager.super_user:
        sendingMessagesManager = SendingMessagesManager()
        list_user_for_sending = sendingMessagesManager.user_sending

        for user in list_user_for_sending:
            responseMan = ResponseManager(user_id=user[1], message=update.message.text)
            responseMan.response_to_invitation_question()

            template = sendingMessagesManager.get_template_sending_with_name() % responseMan.user_name_mf
            # await context.bot.send_message(chat_id=id,text=template)

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
    responseManager = ResponseManager(user_id=update.effective_user.id, message='-',
                                      photo_id=update.message.photo[0].file_id)
    if responseManager.super_user:
        if responseManager.user_state == 4:  # ожидание текста поста
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Требуется текст!')
        elif responseManager.user_state == 5:
            response = responseManager.add_image_id_in_post()
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=response)

    """
    newFile = update.message.photo
    # newFile[0].file_id = 'AgACAgIAAxkBAAIBi2P_xRIa8MH9DzVPXZ5DBRrWvYdEAAIlzDEbjqj5S4e9uvP_dIr0AQADAgADbQADLgQ'

    print(newFile[0])
    print(newFile[1])

    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo='AgACAgIAAxkBAAIBlWP_xu6r84PjlgAB38gOpzvMEoSXogACLcwxG46o-Uu1VpAc_71ufgEAAwIAA20AAy4E')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='test')
    newFile.download('img_'+update.message.photo[-1].file_id+'.png')
    with open('img_' + f_id + '.jpg', 'wb') as file:
        file.write(down_file)
    AgACAgIAAxkBAAIBi2P_xRIa8MH9DzVPXZ5DBRrWvYdEAAIlzDEbjqj5S4e9uvP_dIr0AQADAgADbQADLgQ
    bot = update.get_bot()
    print('bot', bot)
    print('update.message.photo[0] - ', update.message.photo[0])
    file_photo = bot.get_file(update.message.photo[0])
    print('file_photo', file_photo)
    src = '/' + update.message.photo[0].file_id
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    #encoded_string = base64.b64encode(p)
    #print(encoded_string)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo[0])

    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    response = responseManager.generate_response_with_name()

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)"""


# '👍😅🙃😂😘❤️😍😊😁'
# 👍😅🙃😂😘❤️😍😊😁


# test group sending
async def group_sending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    if responseManager.get_user_lvl():
        responseManager.set_user_state(4)


"""        sendingMessagesManager = SendingMessagesManager()
        list_user_for_sending = sendingMessagesManager.user_sending

        for user in list_user_for_sending:
            responseMan = ResponseManager(user_id=user[1], message=update.message.text)
            responseMan.response_to_invitation_question()

            template = sendingMessagesManager.get_template_sending_with_name() % responseMan.user_name_mf
            # await context.bot.send_message(chat_id=id,text=template)
            send = [InlineKeyboardButton("Приду на игры", callback_data='+')]
            send2 = [InlineKeyboardButton("Не приду на игры", callback_data='-')]
            keyboard = [
                send,
                send2
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=responseMan.user_id, text=template, reply_markup=reply_markup)

        response = responseManager.generate_response_for_super_user_sending(name=responseManager.user_name_mf)

        await context.bot.send_message(chat_id=responseManager.user_id,
                                       text=response)
    else:
        response = responseManager.generate_response_for_default_user_sending(name=responseManager.user_name_mf)
        await context.bot.send_message(chat_id=responseManager.user_id,
                                       text=response)"""


def test_mod():
    # bdConnect.get_post(1)
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


async def post_builder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('echo', update.message.text)
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    if responseManager.super_user:
        responseManager.add_new_post()
        response = responseManager.generate_response_no_name()
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=response)


if __name__ == '__main__':
    test_mod()

    application = ApplicationBuilder().token(TokenBot).build()

    start_handler = CommandHandler('start', start)

    post_builder_handler = CommandHandler('PostBuilder', post_builder)
    sending_handler = CommandHandler('sending', sending)
    # group_sending_handler = CommandHandler('group', post_builder)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND), photo)

    application.add_handler(CallbackQueryHandler(response_to_invitation))

    application.add_handler(start_handler)

    application.add_handler(post_builder_handler)
    application.add_handler(sending_handler)

    # application.add_handler(group_sending_handler)

    application.add_handler(echo_handler)
    application.add_handler(photo_handler)

    application.run_polling()
