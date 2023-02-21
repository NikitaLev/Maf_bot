import random

from BDconnect import BDconnect
import Dictionary

bdConnector = BDconnect()


class SendingMessagesManager:
    def __init__(self):
        print(bdConnector.get_user_with_state_sending('1'))
    def get_template(self):
        return random.choice(Dictionary.template_post)

