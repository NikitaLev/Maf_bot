import sqlite3
import Dictionary


class BDconnect:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect("bot.db")
        self.create_db()

    def create_db(self):
        cursor = self.sqlite_connection.cursor()

        cursor.execute("""CREATE TABLE if not exists User
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        name TEXT, 
                        user_id INTEGER,
                        mafia_name TEXT,
                        state INTEGER,
                        message_history json,
                        id_last_message id)
                    """)

        cursor.execute("""CREATE TABLE if not exists Message
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        user_id INTEGER,
                        message TEXT)
                    """)
        cursor.close()

    def insert_user(self, name, user_id, mafia_name):
        user = (name, user_id, mafia_name, 0, '', 0)
        if len(self.check_user(user_id)) == 0:
            cursor = self.sqlite_connection.cursor()
            cursor.execute("INSERT INTO User (name, user_id, mafia_name, state, message_history, id_last_message) "
                           "VALUES (?, ?, ?, ?, ?, ?)", user)
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
        print('get_user_state ',self.get_user_state(user_id))
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


    def test(self):
        user_id = 490466369
        cursor = self.sqlite_connection.cursor()
        sql_req = 'SELECT mafia_name FROM User where user_id = %s' % str(user_id)
        cursor.execute(sql_req)
        res = cursor.fetchall()
        res1 = res[0]
        res = res1[0]
        print(sql_req, res, res1)
        self.sqlite_connection.commit()
        cursor.close()


