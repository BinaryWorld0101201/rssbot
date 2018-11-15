import logging
from datetime import datetime, timedelta
from time import mktime

import feedparser

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
        except (AttributeError, IndexError):
            logging.info('{} could not be parsed'.format(url))
            return []
        entries = []
        for item in d.entries:
            try:
                if time < datetime.fromtimestamp(mktime(item.updated_parsed)):
                    entries.append((item.title, item.link))
                else:
                    break
            except AttributeError:
                logging.info('{} could not be parsed'.format(url))

        self.database.update_urls_time(url, str(last_update_time))
        return entries

    def find_all_urls(self):
        return self.database.find_urls()

    def find_chats_by_url(self, url):
        return self.database.find_chats_by_url(url)

    def list(self, chat_id):
        url_name = []
        for url in self.database.find_urls_by_chat_id(chat_id):
            name = self.database.find_name_by_url(url)
            url_name.append((url, name))
        return url_name


if __name__ == '__main__':
    rss = RSSFetcher()
    url = 'https://nierunjie.github.io/atom.xml'
    d = feedparser.parse(url)
    print(d.entries)
