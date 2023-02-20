import random

from BDconnect import BDconnect
import Dictionary

bdConnector = BDconnect()


class ResponseManager:

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.user_name_mf = self.get_user_name_mf()
        self.user_state = self.get_state_user()
        if self.user_state == 2:
            self.set_user_name_mf()
            self.user_name_mf = self.get_user_name_mf()
            self.set_user_state(3)


    def get_state_user(self):
        return int(bdConnector.get_user_state(self.user_id))

    def get_user_name_mf(self):
        return bdConnector.get_user_name_mf(self.user_id)

    def set_user_state(self, state):
        self.user_state = state
        print('state-', state)
        bdConnector.set_user_state(user_id=self.user_id, state=state)
    def set_user_name_mf(self):
        return bdConnector.update_user_mafia_name(self.user_id, self.message)

    def generate_response_no_name(self):
        response = Dictionary.response_template_in_state.get(self.user_state)
        result = random.choice(response)
        return result

    def generate_response_with_name(self):
        response = Dictionary.response_template_in_state.get(self.user_state)
        print(response, self.user_state)
        result = random.choice(response)
        result = result % self.user_name_mf
        if self.user_name_mf == 3:
            self.set_user_state(1)

        return result



