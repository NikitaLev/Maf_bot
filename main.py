import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import Data_file


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(Data_file.Token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
