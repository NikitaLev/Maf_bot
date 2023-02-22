import random

from BDconnect import BDconnect
import Dictionary

bdConnector = BDconnect()


class SendingMessagesManager:
    def __init__(self):
        self.user_sending = bdConnector.get_user_with_state_sending('1')

    def get_template_sending_no_name(self):
        return random.choice(Dictionary.template_no_name_post)

    def get_template_sending_with_name(self):
        return random.choice(Dictionary.template_post_with_name)
