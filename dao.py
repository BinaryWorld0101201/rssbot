import logging
import sqlite3


class SQLiteDB(object):
    def __init__(self):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        try:
            self.find_urls()
        except sqlite3.OperationalError:
            sql = """
            CREATE TABLE URLS( URL VARCHAR(255) PRIMARY KEY NOT NULL, NAME VARCHAR(255) NOT NULL, LAST_UPDATE DATETIME DEFAULT (datetime('now')), PUSH INTGER DEFAULT 0);
            CREATE TABLE RELATION( URL VARCHAR(255) NOT NULL, CHAT_ID CHARACTER(20) NOT NULL, PRIMARY KEY(URL,CHAT_ID));
            CREATE TRIGGER IF NOT EXISTS clear AFTER DELETE ON RELATION WHEN (SELECT URL FROM RELATION WHERE URL=OLD.URL LIMIT 1) ISNULL BEGIN DELETE FROM URLS WHERE URL=OLD.URL; END; 
            """
            cursor.executescript(sql)

        conn.commit()
        cursor.close()
        conn.close()

    def insert_url(self, url, name):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO URLS(URL,NAME) VALUES(?,?);"
            cursor.execute(sql, (url, name))
        except sqlite3.IntegrityError:
            pass
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def insert_relation(self, url, chat_id):
        ret = True
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        try:
            sql = "INSERT INTO RELATION VALUES(?,?)"
            cursor.execute(sql, (url, str(chat_id)))
        except sqlite3.IntegrityError:
            pass
        except:
            ret = False
        conn.commit()
        cursor.close()
        conn.close()
        return ret

    def delete_relation(self, url, chat_id):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "DELETE FROM RELATION WHERE URL=? AND CHAT_ID=?;"
        cursor.execute(sql, (url, str(chat_id)))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def delete_all_relation_by_id(self, chat_id):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "DELETE FROM RELATION WHERE CHAT_ID=?;"
        cursor.execute(sql, (str(chat_id),))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def find_urls_by_chat_id(self, chat_id):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT URL FROM RELATION WHERE CHAT_ID =?;"
        cursors = cursor.execute(sql, (str(chat_id),))
        urls = []
        for item in cursors:
            urls.append(item[0])
        cursor.close()
        conn.close()
        return urls

    def find_chats_by_url(self, url):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT CHAT_ID FROM RELATION WHERE URL =?;"
        cursors = cursor.execute(sql, (str(url),))
        chats = []
        for item in cursors:
            chats.append(item[0])
        cursor.close()
        conn.close()
        return chats

    def update_urls_time(self, url, time):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "UPDATE URLS SET LAST_UPDATE =? WHERE URL=?;"
        cursor.execute(sql, (time, url))
        conn.commit()
        cursor.close()
        conn.close()

    def update_push(self, url, push):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "UPDATE URLS SET PUSH =? WHERE URL=?;"
        cursor.execute(sql, (push, url))
        conn.commit()
        cursor.close()
        conn.close()

    def find_urls(self):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT URL FROM URLS;"
        cursors = cursor.execute(sql)
        urls = []
        for item in cursors:
            urls.append(item[0])
        cursor.close()
        conn.close()
        return urls

    def delete_url(self, url):
        chats = self.find_chats_by_url(url)
        for chat_id in chats:
            self.delete_relation(url, chat_id)

    def find_push(self, url):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT PUSH FROM URLS WHERE URL=?;"
        cursors = cursor.execute(sql, (url,))
        ret = cursors.fetchone()[0]
        cursor.close()
        conn.close()
        return ret

    def find_time_by_url(self, url):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT LAST_UPDATE FROM URLS WHERE URL=?;"
        cursors = cursor.execute(sql, (url,))
        ret = cursors.fetchone()[0]
        cursor.close()
        conn.close()
        return ret

    def find_name_by_url(self, url):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT NAME FROM URLS WHERE URL=?;"
        cursors = cursor.execute(sql, (url,))
        ret = cursors.fetchone()[0]
        cursor.close()
        conn.close()
        return ret

    def find_all_url_and_name(self):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT URL,NAME FROM URLS"
        cursors = cursor.execute(sql)
        ret = []
        for item in cursors:
            ret.append([item[0], item[1]])
        cursor.close()
        conn.close()
        return ret

    def find_pushed_url_and_name(self):
        conn = sqlite3.connect('rss.db')
        cursor = conn.cursor()

        sql = "SELECT URL,NAME FROM URLS WHERE PUSH = 1"
        cursors = cursor.execute(sql)
        ret = []
        for item in cursors:
            ret.append([item[0], item[1]])
        cursor.close()
        conn.close()
        return ret


if __name__ == '__main__':
    from datetime import datetime
    db = SQLiteDB()
    ret = db.find_push("https://www.solidot.org/index.rss")
    print(ret != True)
