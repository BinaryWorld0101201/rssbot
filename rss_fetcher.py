import feedparser
import sqlite3
from datetime import datetime, timedelta
from time import mktime
from dao import SQLiteDB


class RSSFetcher(object):
    def __init__(self):
        self.database = SQLiteDB()

    def is_valid_url(self, url):
        d = feedparser.parse(url)
        try:
            return d.entries[0].updated_parsed and d.feed.title
        except:
            return False

    def subscribe(self, url, chat_id):
        name = self.is_valid_url(url)
        if not name:
            return False
        self.database.insert_url(url, name)
        return self.database.insert_relation(url, chat_id)

    def unsubscribe(self, url, chat_id):
        self.database.delete_relation(url, chat_id)

    def get_entries(self, url):
        d = feedparser.parse(url)
        time = datetime.fromisoformat(self.database.find_time_by_url(url))
        try:
            last_update_time = datetime.fromtimestamp(
                mktime(d.entries[0].updated_parsed))
        except AttributeError or IndexError:
            last_update_time = str(datetime.utcnow()).split('.')[0]
        entries = []
        for item in d.entries:
            if time < datetime.fromtimestamp(mktime(item.published_parsed)):
                entries.append((item.title, item.link))

        self.database.update_urls_time(url, str(last_update_time))
        return entries

    def find_all_urls(self):
        return self.database.find_urls()

    def find_chats_by_url(self, url):
        return self.database.find_chats_by_url(url)

    def list(self, url):
        return self.database.find_urls_by_chat_id(url)


if __name__ == '__main__':
    rss = RSSFetcher()
    rss.update()
