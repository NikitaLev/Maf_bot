import sqlite3
import DatabaseManager
import Dictionary

from DatabaseManager import DatabaseManager


class BDconnect:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.sqlite_connection = sqlite3.connect(self.db_manager.name_bd)

    def insert_user(self, name, user_id, mafia_name):
        user = (name, user_id, mafia_name, 0, '', 0, True, False, False, 0)
        if len(self.check_user(user_id)) == 0:
            cursor = self.sqlite_connection.cursor()
            cursor.execute("INSERT INTO User (name, user_id, mafia_name, state, message_history, id_last_message, "
                           "sending_message, super_user, invitation_status, id_post_create)"
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user)
            self.sqlite_connection.commit()
            cursor.close()

    def insert_post(self, user_id):
        post = (1, user_id, '-', '-', 0)
        cursor = self.sqlite_connection.cursor()
        cursor.execute("INSERT INTO Post (active_post, user_id, text_post, photo_id, count_user_will_be) "
                       "VALUES (?, ?, ?, ?, ?)", post)
        self.sqlite_connection.commit()
        cursor.close()
        self.add_post_for_user(user_id, self.get_last_id_post())

    def get_last_id_post(self):
        cursor = self.sqlite_connection.cursor()
        sql_req = """SELECT
                          id
                        FROM
                          Post
                        ORDER BY
                          id DESC
                        LIMIT 1"""
        cursor.execute(sql_req)
        res = cursor.fetchall()
        res1 = res[0]
        res = res1[0]
        print(res)
        cursor.close()
        return res

    def get_actove_post_list(self):
        cursor = self.sqlite_connection.cursor()
        sql_req = """SELECT
                          user_id
                        FROM
                          Post
                        WHERE
                        active_post = 1
                        ORDER BY
                          id DESC
                        LIMIT 1"""
        cursor.execute(sql_req)
        res = cursor.fetchall()
        return res

    def add_post_for_user(self, user_id, post_id):
        cursor = self.sqlite_connection.cursor()
        data = (post_id, user_id)
        cursor.execute("""UPDATE User
                       SET id_post_create = ?
                       WHERE user_id = ?""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def add_text_in_post(self, text, id_post):
        cursor = self.sqlite_connection.cursor()
        data = (text, id_post)
        cursor.execute("""UPDATE Post
                       SET text_post = ?
                       WHERE id = ?""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def add_photo_id_in_post(self, photo_id, id_post):
        cursor = self.sqlite_connection.cursor()
        data = (photo_id, id_post)
        cursor.execute("""UPDATE Post
                       SET photo_id = ?
                       WHERE id = ?""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def get_post_user(self, user_id):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT id_post_create FROM User where user_id = %s' % str(user_id)
        cursor.execute(sql_req)
        res = cursor.fetchall()
        res1 = res[0]
        res = res1[0]
        cursor.close()
        return res

    def get_post(self, post_id):
        cursor = self.sqlite_connection.cursor()
        print('post_id', post_id, type(post_id))
        sql_req = 'SELECT * FROM Post'
        cursor.execute("""SELECT * FROM Post
                       WHERE id =? """, str(post_id))
        res = cursor.fetchall()
        res1 = res[0]
        cursor.close()
        return res1

    def deactivation_post(self, post_id):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""UPDATE Post
                       SET active_post = 0
                       WHERE id = ?""", str(post_id))
        self.sqlite_connection.commit()
        cursor.close()

    def deactivation_app_post(self):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""UPDATE Post
                       SET active_post = 0
                       WHERE active_post = 1""")
        self.sqlite_connection.commit()
        cursor.close()

    def break_user_post(self, user_id):
        cursor = self.sqlite_connection.cursor()
        data = (0, user_id)
        print(user_id)
        cursor.execute("""UPDATE User
                       SET id_post_create = ?
                       WHERE user_id = ?;""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def break_invitation_status(self):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""UPDATE User
                       SET invitation_status = 0
                       WHERE invitation_status = 1;""")
        self.sqlite_connection.commit()
        cursor.close()

    def check_user(self, user_id):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT * FROM User where user_id = %s' % str(user_id)
        cursor.execute(sql_req)
        res = cursor.fetchall()
        cursor.close()
        return res

    def update_user_mafia_name(self, user_id, mafia_name):
        cursor = self.sqlite_connection.cursor()
        data = (mafia_name, user_id)
        cursor.execute("""UPDATE User
                       SET mafia_name = ?
                       WHERE user_id = ?""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def update_user_state_sending(self, user_id, state_sending):
        cursor = self.sqlite_connection.cursor()
        data = (state_sending, user_id)
        cursor.execute("""UPDATE User
                       SET sending_message = ?
                       WHERE user_id = ?""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def get_user_state(self, user_id):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT state FROM User where user_id = %s' % str(user_id)
        cursor.execute(sql_req)
        res = cursor.fetchall()
        res1 = res[0]
        res = res1[0]
        cursor.close()
        return res

    def set_user_state(self, user_id, state):
        cursor = self.sqlite_connection.cursor()
        data = (state, user_id)
        cursor.execute("""UPDATE User
                       SET state = ?
                       WHERE user_id = ?;""", data)
        print('get_user_state ', self.get_user_state(user_id))
        self.sqlite_connection.commit()
        cursor.close()

    def get_user_name_mf(self, user_id):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT mafia_name FROM User where user_id = %s' % str(user_id)
        cursor.execute(sql_req)
        res = cursor.fetchall()
        res1 = res[0]
        res = res1[0]
        cursor.close()
        return res

    def insert_message(self, user_id, message):
        message = (user_id, message)
        cursor = self.sqlite_connection.cursor()
        cursor.execute("INSERT INTO Message (user_id, message) VALUES (?, ?)", message)
        self.sqlite_connection.commit()
        cursor.close()

    def get_user_with_state_sending(self, state_sending):
        cursor = self.sqlite_connection.cursor()
        print(state_sending)
        cursor.execute('SELECT mafia_name, user_id FROM User where sending_message = ?', state_sending)
        res = cursor.fetchall()
        # res = res[0]
        # print(res[0],res[1])
        cursor.close()
        return res

    def set_super_user_level(self, user_id):
        cursor = self.sqlite_connection.cursor()
        data = (True, user_id)
        cursor.execute("""UPDATE User
                               SET super_user = ?
                               WHERE user_id = ?;""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def set_default_user_level(self, user_id):
        cursor = self.sqlite_connection.cursor()
        data = (False, user_id)
        cursor.execute("""UPDATE User
                               SET super_user = ?
                               WHERE user_id = ?;""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def get_user_level(self, user_id):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT super_user FROM User where user_id = %s' % str(user_id)
        cursor.execute(sql_req)
        res = cursor.fetchall()
        res1 = res[0]
        res = res1[0]
        cursor.close()
        return res

    def set_user_invitation_status(self, status, user_id):
        cursor = self.sqlite_connection.cursor()
        data = (status, user_id)
        print('data', data)
        cursor.execute("""UPDATE User
                               SET invitation_status = ?
                               WHERE user_id = ?;""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def add_user_in_post(self):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""UPDATE Post
                       SET count_user_will_be = count_user_will_be + 1
                       WHERE active_post = 1""")
        self.sqlite_connection.commit()
        cursor.close()

    def test(self, user_id, test_P):
        cursor = self.sqlite_connection.cursor()
        data = (test_P, user_id)
        print('data', data)
        cursor.execute("""UPDATE User
                               SET invitation_status = ?
                               WHERE user_id = ?;""", data)
        self.sqlite_connection.commit()
        cursor.close()

    def test_insert_user(self, name, user_id, mafia_name):
        user = (name, user_id, mafia_name, 0, '', 0, True, False, False)
        if len(self.check_user(user_id)) == 0:
            cursor = self.sqlite_connection.cursor()
            cursor.execute("INSERT INTO User (name, user_id, mafia_name, state, message_history, id_last_message, "
                           "sending_message, super_user, invitation_status)"
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user)
            self.sqlite_connection.commit()
            cursor.close()

    def who_marked_true(self):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT mafia_name FROM User where invitation_status = 1'
        cursor.execute(sql_req)
        res = cursor.fetchall()
        cursor.close()
        return res

    def who_marked_maybe(self):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT mafia_name FROM User where invitation_status = 2'
        cursor.execute(sql_req)
        res = cursor.fetchall()
        cursor.close()
        return res

    def check_user_invitation_status(self, user_id):
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT invitation_status FROM User where user_id = ' + str(user_id)
        cursor.execute(sql_req)
        res = cursor.fetchall()[0][0]
        cursor.close()
        return res

    def delete_user_in_post(self):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""UPDATE Post
                       SET count_user_will_be = count_user_will_be - 1
                       WHERE active_post = 1""")
        self.sqlite_connection.commit()
        cursor.close()
