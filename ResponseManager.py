import random

from BDconnect import BDconnect
import Dictionary

bdConnector = BDconnect()


def get_user_name_mf(user_id):
    return bdConnector.get_user_name_mf(user_id)


class ResponseManager:

    def __init__(self, user_id, message='-', photo_id='-'):
        self.user_id = user_id
        self.message = message
        self.photo_id = photo_id
        self.user_name_mf = self.get_user_name_mf()
        self.user_state = self.get_state_user()
        self.super_user = self.get_user_lvl()
        self.user_post = 0
        if self.super_user and self.user_state > 3:
            self.user_post = self.get_user_post()
        if self.user_state == 2:
            self.set_user_name_mf()
            self.user_name_mf = self.get_user_name_mf()
            self.set_user_state(3)

    def get_data_post_user(self):
        return bdConnector.get_post(self.user_post)

    def not_recognized_text(self):
        response = Dictionary.not_recognized
        result = random.choice(response)
        return result

    def deactivation_post_user(self):
        response = Dictionary.deactivation_post
        bdConnector.deactivation_post(post_id=self.user_post)
        bdConnector.break_user_post(user_id=self.user_id)
        self.set_user_state(1)
        result = random.choice(response)
        return result

    def add_text_in_post(self):
        bdConnector.add_text_in_post(self.message, self.user_post)
        self.set_user_state(5)
        return self.generate_response_no_name()

    def add_image_id_in_post(self):
        bdConnector.add_photo_id_in_post(self.photo_id, self.user_post)
        self.set_user_state(6)
        return self.generate_response_no_name() + str(self.user_post)

    def add_new_post(self):
        bdConnector.insert_post(self.user_id)
        self.set_user_state(4)
        return self.generate_response_no_name()

    def get_user_post(self):
        return bdConnector.get_post_user(self.user_id)

    def get_user_lvl(self):
        return bdConnector.get_user_level(self.user_id)

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
        if self.user_state == 3:
            self.set_user_state(1)
        return result

    def generate_response_for_super_user_sending(self, name):
        response = Dictionary.response_for_super_user_sending
        result = random.choice(response) % name
        return result

    def generate_response_for_default_user_sending(self, name):
        response = Dictionary.response_for_default_user_sending
        result = random.choice(response) % name
        return result

    def response_to_invitation_true(self):
        response = Dictionary.response_to_invitation_true

        bdConnector.set_user_invitation_status(1, self.user_id)

        result = random.choice(response)
        return result

    def response_to_invitation_false(self):
        response = Dictionary.response_to_invitation_false
        bdConnector.set_user_invitation_status(0, self.user_id)
        result = random.choice(response)
        return result

    def response_to_invitation_question(self):
        response = Dictionary.response_to_invitation_question
        bdConnector.set_user_invitation_status(2, self.user_id)
        result = random.choice(response)
        return result

    def response_have_active_post(self, user_id):
        response = Dictionary.response_have_active_post
        name = get_user_name_mf(user_id)
        result = random.choice(response) % name
        return result




