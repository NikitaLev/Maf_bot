import sqlite3
import Data_file



class DatabaseManager:
    def __init__(self):
        self.name_bd = Data_file.NameDB
        self.sqlite_connection = sqlite3.connect(self.name_bd)
        self.create_db()
        #self.extension_bd()

    def create_db(self):
        cursor = self.sqlite_connection.cursor()

        cursor.execute("""CREATE TABLE if not exists User
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        name TEXT, 
                        user_id INTEGER,
                        mafia_name TEXT,
                        state INTEGER,
                        message_history json,
                        id_last_message INTEGER,
                        sending_message NUMERIC,
                        super_user NUMERIC,
                        invitation_status INTEGER,
                        arrives_time TEXT
                        id_post_create INTEGER)
                    """)

        cursor.execute("""CREATE TABLE if not exists Message
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        user_id INTEGER,
                        message TEXT)
                    """)
        cursor.execute("""CREATE TABLE if not exists Post
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        active_post NUMERIC, 
                        user_id INTEGER,
                        text_post TEXT,
                        photo_id INTEGER,
                        count_user_will_be INTEGER,
                        post_type NUMERIC)
                    """)
        cursor.close()

    def extension_bd(self):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""ALTER TABLE Post ADD COLUMN post_type NUMERIC DEFAULT 0""")
        cursor.close()
