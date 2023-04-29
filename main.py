import asyncio
import logging
import random
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
from RatingManager import RatingManager
from ResponseManager import ResponseManager
from SendingMessagesManager import SendingMessagesManager

import Dictionary

bdConnect = BDconnect()
TokenBot = Data_file.Token
# bot = telegram.Bot(TokenBot)

persent_rec = 50

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

"""async def test():
    await bot.send_message(chat_id=490466369, text='test')"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(3)
    bdConnect.insert_user(name=update.effective_user.full_name, user_id=update.effective_user.id, mafia_name="-")

    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    response = responseManager.generate_response_no_name()
    responseManager.set_user_state(2)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('echo ', update.message.text)
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    recognize_result = recognize_cmd(responseManager.message)
    if responseManager.user_invitation_state == 3:
        time = get_time_invitation(responseManager.message)

        response = ''
        if not time in Dictionary.error_time_invitation.keys():
            response = responseManager.response_to_invitation_set_time()
        else:
            response = Dictionary.error_time_invitation.get(time)
            response = random.choice(response)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=response)
        return

    if recognize_result['cmd'] == "who_marked" and recognize_result['percent'] > persent_rec:
        response = responseManager.who_marked()
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=response)
        return
    if responseManager.super_user:
        if recognize_result['cmd'] == "info_post_create" and recognize_result['percent'] > persent_rec:
            active_post_list = bdConnect.get_active_info_post_list()
            if len(active_post_list) == 0:
                responseManager.add_new_post(1)
                response = responseManager.generate_response_no_name()
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=response)
            else:
                user_id_active_post = active_post_list[0][0]
                response = responseManager.response_have_active_post(user_id=user_id_active_post)
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=response)
            return

        if responseManager.user_state <= 5 and ((recognize_result['cmd'] == "not" or recognize_result['cmd'] == "deactivation_post") \
                and recognize_result['percent'] > persent_rec):
            response = responseManager.deactivation_last_post()
            await context.bot.send_message(chat_id=responseManager.user_id,
                                           text=response)
            return 0
        elif responseManager.user_state == 4:  # ожидание текста поста
            response = responseManager.add_text_in_post()
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=response)
            return
        elif responseManager.user_state == 5:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Требуется фото')
            return
        elif responseManager.user_state == 6:

            text_data = ''
            photo_data = ''
            reply_markup = ''
            if responseManager.message.isdigit():
                text_data, photo_data, reply_markup = post_creator(bdConnect.get_post(responseManager.message))
                responseManager.set_user_state(7)
            else:
                if (recognize_result['cmd'] == "sending_command" or recognize_result['cmd'] == "yes") \
                        and recognize_result['percent'] > persent_rec:
                    text_data, photo_data, reply_markup = post_creator(responseManager.get_data_post_user())
                    responseManager.set_user_state(7)
                elif (recognize_result['cmd'] == "not" or recognize_result['cmd'] == "deactivation_post") \
                        and recognize_result['percent'] > persent_rec:
                    response = responseManager.deactivation_post_user()
                    await context.bot.send_message(chat_id=responseManager.user_id,
                                                   text=response)
                    return 0
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
                await context.bot.send_photo(chat_id=responseMan.user_id,
                                             photo=photo_data)

                if responseManager.get_user_post_type() == 1:
                    await context.bot.send_message(chat_id=responseManager.user_id,
                                                   text=template)
                    responseManager.deactivation_info_post_user()
                else:
                    await context.bot.send_message(chat_id=responseMan.user_id, text=template, reply_markup=reply_markup)

            response = responseManager.generate_response_for_super_user_sending(name=responseManager.user_name_mf)

            await context.bot.send_message(chat_id=responseManager.user_id,
                                           text=response)
            return
        elif responseManager.user_state == 7:
            if recognize_result['cmd'] == "deactivation_post" \
                    and recognize_result['percent'] > persent_rec:
                response = responseManager.generate_response_no_name()
                responseManager.deactivation_post_user()
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=response)
    else:
        response = responseManager.generate_response_with_name()

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=response)


def get_time_invitation(time):
    if ':' in time:
        h, m = time.split(':')
        if h.isdigit():
            if m.isdigit():
                return time
            else:
                return 'M'
        else:
            return 'H'
    else:
        return ':'


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
    keyboard = [
        [InlineKeyboardButton("Приду на игры", callback_data='+')],
        [InlineKeyboardButton("В следующий раз", callback_data='-')],
        [InlineKeyboardButton("Пока не знаю", callback_data='?'),
         InlineKeyboardButton("Опоздаю", callback_data='time')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if data:
        return data[3], data[4], reply_markup


"""    keyboard = [
        [InlineKeyboardButton("Приду на игры", callback_data='+')],
        [InlineKeyboardButton("В следующий раз", callback_data='-')],
        [InlineKeyboardButton("Пока не знаю", callback_data='?')]
    ]"""

"""async def sending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    if responseManager.super_user:
        sendingMessagesManager = SendingMessagesManager()
        list_user_for_sending = sendingMessagesManager.user_sending

        for user in list_user_for_sending:
            responseMan = ResponseManager(user_id=user[1], message=update.message.text)
            responseMan.response_to_invitation_question()

            template = sendingMessagesManager.get_template_sending_with_name() % responseMan.user_name_mf
            # await context.bot.send_message(chat_id=id,text=template)


            await context.bot.send_message(chat_id=responseMan.user_id, text=template, reply_markup=reply_markup)

        response = responseManager.generate_response_for_super_user_sending(name=responseManager.user_name_mf)

        await context.bot.send_message(chat_id=responseManager.user_id,
                                       text=response)
    else:
        response = responseManager.generate_response_for_default_user_sending(name=responseManager.user_name_mf)
        await context.bot.send_message(chat_id=responseManager.user_id,
                                       text=response)"""


async def response_to_invitation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(2)
    active_post_list = bdConnect.get_active_post_list()
    query = update.callback_query
    variant = query.data
    if len(active_post_list) == 1:
        template = ''
        responseManager = ResponseManager(user_id=update.effective_user.id, message=variant)
        if variant == '+':
            template = responseManager.response_to_invitation_true()
        elif variant == '-':
            template = responseManager.response_to_invitation_false()
        elif variant == 'time':
            template = responseManager.response_to_invitation_in_time()
        else:
            template = responseManager.response_to_invitation_question()
        await context.bot.send_message(chat_id=responseManager.user_id, text=template)
    else:
        responseManager = ResponseManager(user_id=update.effective_user.id, message=variant)
        template = responseManager.all_post_deactife()
        await context.bot.send_message(chat_id=responseManager.user_id, text=template)


"""    await query.answer()
    await query.edit_message_text(text=f"Выбранный вариант: {variant}")
    keyboard = [
        [InlineKeyboardButton("Приду на игры", callback_data='test')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)"""


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(1)
    responseManager = ResponseManager(user_id=update.effective_user.id, message='-',
                                      photo_id=update.message.photo[0].file_id)
    if responseManager.super_user:
        if responseManager.user_state == 4:  # ожидание текста поста
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Требуется текст!')
        elif responseManager.user_state == 5:
            response = responseManager.add_image_id_in_post()
            text_data, photo_data, reply_markup = post_creator(responseManager.get_data_post_user())
            await context.bot.send_photo(chat_id=update.effective_chat.id,
                                         photo=photo_data)

            if responseManager.get_user_post_type() == 1:
                await context.bot.send_message(chat_id=responseManager.user_id,
                                               text=text_data)
            else:
                await context.bot.send_message(chat_id=responseManager.user_id, text=text_data, reply_markup=reply_markup)

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=response)


async def documentExcel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('11111111111111111111111111111111111111111111')
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive(update.message.document.file_name)
    ratingManager = RatingManager(update.message.document.file_name)
    print(update.message)
    print(update.message.document)
    print(update.message.document.file_id)

    responseManager = ResponseManager(user_id=update.effective_user.id, message='-',
                                      photo_id=update.message.document.file_id)
    print(responseManager.doc_id)
    #await context.bot.send_document(chat_id=update.effective_chat.id,
                                    #document=responseManager.doc_id)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Файл принят")

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
    bdConnect.test_del_user_bd(299686106)
    #bdConnect.test_del_user_bd(451591039)

    #bdConnect.test_del_user_bd(22222)

    # bdConnect.get_post(1)
    # bdConnect.set_super_user_level(490466369)
"""    bdConnect.insert_user(name='test1', user_id=11111, mafia_name="test1")
    bdConnect.test(user_id=11111, test_P=1)
    bdConnect.insert_user(name='test2', user_id=22222, mafia_name="test2")
    bdConnect.test(user_id=22222, test_P=2)
    #bdConnect.deactivation_all_post()
    #bdConnect.set_user_invitation_status(0, 490466369)
    #bdConnect.set_user_state(1, 490466369)
    # list = bdConnect.who_marked_true()
    # lis1t = bdConnect.who_marked_true()[0]
    # lis1t2 = lis1t[0]
    # bdConnect.deactivation_app_post()
    print(len(bdConnect.get_actove_post_list()) == 0)
    
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
    asyncio.run(test)    490466369
"""


# создание поста
async def post_builder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('echo', update.message.text)
    responseManager = ResponseManager(user_id=update.effective_user.id, message=update.message.text)
    if responseManager.super_user:
        active_post_list = bdConnect.get_active_post_list()
        if len(active_post_list) == 0:
            responseManager.add_new_post(0)
            response = responseManager.generate_response_no_name()
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=response)
        else:
            user_id_active_post = active_post_list[0][0]
            response = responseManager.response_have_active_post(user_id=user_id_active_post)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=response)


if __name__ == '__main__':
    test_mod()

    application = ApplicationBuilder().token(TokenBot).build()

    start_handler = CommandHandler('start', start)

    post_builder_handler = CommandHandler('PostBuilder', post_builder)
    # sending_handler = CommandHandler('sending', sending)
    # group_sending_handler = CommandHandler('group', post_builder)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    photo_handler = MessageHandler(filters.PHOTO & (~filters.COMMAND), photo)
    doc_handler = MessageHandler(filters.Document.ALL, documentExcel)
    application.add_handler(CallbackQueryHandler(response_to_invitation))

    application.add_handler(start_handler)

    application.add_handler(post_builder_handler)
    # application.add_handler(sending_handler)

    # application.add_handler(group_sending_handler)

    application.add_handler(echo_handler)
    application.add_handler(photo_handler)
    application.add_handler(doc_handler)

    application.run_polling()
