import random

from BDconnect import BDconnect
import Dictionary

bdConnector = BDconnect()


class SendingMessagesManager:
    def __init__(self):
        print(bdConnector.get_user_with_state_sending('1'))

    def sending_message(self):
        bdConnector.get_user_with_state_sending('1')

