import sqlite3
import logging


class SQLiteDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('rss.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def insert_url(self, url, name):
        try:
            sql = "INSERT INTO URLS(URL,NAME) VALUES(?,?);"
            self.cursor.execute(sql, (url, name))
        except sqlite3.IntegrityError:
            pass
        self.conn.commit()
        return True

    def insert_relation(self, url, chat_id):
        ret = True
        try:
            sql = "INSERT INTO RELATION VALUES(?,?)"
            self.cursor.execute(sql, (url, str(chat_id)))
        except sqlite3.IntegrityError:
            pass
        except:
            ret = False
        self.conn.commit()
        return ret

    def delete_relation(self, url, chat_id):
        sql = "DELETE FROM RELATION WHERE URL=? AND CHAT_ID=?;"
        self.cursor.execute(sql, (url, str(chat_id)))
        self.conn.commit()
        return True

    def find_urls_by_chat_id(self, chat_id):
        sql = "SELECT URL FROM RELATION WHERE CHAT_ID =?;"
        cursors = self.cursor.execute(sql, (str(chat_id),))
        urls = []
        for item in cursors:
            urls.append(item[0])
        return urls

    def find_chats_by_url(self, url):
        sql = "SELECT CHAT_ID FROM RELATION WHERE URL =?;"
        cursors = self.cursor.execute(sql, (str(url),))
        chats = []
        for item in cursors:
            chats.append(item[0])
        return chats

    def update_urls_time(self, url, time):
        sql = "UPDATE URLS SET LAST_UPDATE =? WHERE URL=?;"
        self.cursor.execute(sql, (time, url))
        self.conn.commit()

    def find_urls(self):
        sql = "SELECT URL,LAST_UPDATE FROM URLS;"
        cursors = self.cursor.execute(sql)
        urls = {}
        for item in cursors:
            urls[item[0]] = item[1]
        return urls


if __name__ == '__main__':
    from datetime import datetime
    db = SQLiteDB()
    db.update_urls_time('https://www.zhihu.com/rss', str(datetime.utcnow()))
