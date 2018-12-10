import threading
import logging
import time
import random
from datetime import datetime

from telegram import Bot
from telegram.error import BadRequest, Unauthorized, TimedOut
from telegram.ext import CommandHandler, Job, Updater

from rss_fetcher import RSSFetcher
from start import start
from error import ParseError


class RSSBot(object):
    def __init__(self, token):
        self.bot = Bot(token)
        self.rss_fetcher = RSSFetcher()
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.frequency = 5*60
        self.updater.job_queue.run_repeating(
            self.refresh, self.frequency, first=5)
        self.updater.job_queue.start()
        self.error_times = {}
        self.error_limit = 60

    def subscribe(self, bot, update):
        chat_id = update.message.chat_id
        try:
            url = update.message.text.split(' ')[1]
            ret = self.rss_fetcher.subscribe(url, chat_id)
            if ret:
                name = self.rss_fetcher.database.find_name_by_url(url)
                text = '已订阅:<a href="{}">{}</a>'.format(url, name)
            else:
                text = '订阅失败'
        except IndexError:
            text = '请输入正确的格式\n/sub URL'
        bot.send_message(chat_id, text,
                         parse_mode='HTML',
                         disable_web_page_preview=True)

    def unsubscribe(self, bot, update):
        chat_id = update.message.chat_id
        try:
            url = update.message.text.split(' ')[1]
            name = self.rss_fetcher.database.find_name_by_url(url)
            self.rss_fetcher.unsubscribe(url, chat_id)
            text = '已退订:<a href="{}">{}</a>'.format(url, name)
        except IndexError:
            text = '请输入正确的格式\n/unsub URL'
        except TypeError:
            text = '无此订阅'
        bot.send_message(chat_id, text,
                         parse_mode='HTML',
                         disable_web_page_preview=True)

    def rss(self, bot, update):
        chat_id = update.message.chat_id
        url_name = self.rss_fetcher.list(chat_id)
        text = ""
        if not url_name:
            text = '暂无订阅'
        else:
            for item in url_name:
                text += '<a href="{}">{}</a>\n'.format(item[0], item[1])
        bot.send_message(chat_id, text,
                         parse_mode='HTML',
                         disable_web_page_preview=True)

    def all(self, bot, update):
        chat_id = update.message.chat_id
        url_and_name = self.rss_fetcher.database.find_all_url_and_name()

        text = ''
        for item in url_and_name:
            text += '<a href="{}">{}</a>\n'.format(item[0], item[1])

        bot.send_message(chat_id, text,
                         parse_mode='HTML',
                         disable_web_page_preview=True)

    def push(self, bot, update):
        chat_id = update.message.chat_id
        try:
            url = update.message.text.split(' ')[1]
            ans = self.rss_fetcher.database.find_push(url)
            ret = self.rss_fetcher.database.update_push(url, not ans)
            name = self.rss_fetcher.database.find_name_by_url(url)
            if not ans:
                text = '已推送:<a href="{}">{}</a>'.format(url, name)
            else:
                text = '已取消推送:<a href="{}">{}</a>'.format(url, name)
        except IndexError:
            text = '请输入正确的格式\n/push URL'

        bot.send_message(chat_id, text,
                         parse_mode='HTML',
                         disable_web_page_preview=True)

    def refresh(self, bot, job):
        urls = self.rss_fetcher.find_all_urls()
        delta = self.frequency/len(urls)
        for url in urls:
            threading.Thread(target=self.update, args=(url,)).start()
            time.sleep(delta)

    def update(self, url):
        try:
            entries = self.rss_fetcher.get_entries(url)
            chats = self.rss_fetcher.find_chats_by_url(url)
            self.error_times[url] = 0
            self.send(entries, chats)
            self.broadcast(entries, url)
        except ParseError as e:
            self.error_times[url] = self.error_times.setdefault(url, 0) + 1
            if self.error_times[url] > self.error_limit:
                name = self.rss_fetcher.database.find_name_by_url(url)
                text = '<a href="{}">{} </a>'.format(url, name)
                text += '解析错误次数过多，已被移除，请检查无误后重新订阅'
                chats = self.rss_fetcher.find_chats_by_url(url)
                self.rss_fetcher.database.delete_url(url)
                for chat_id in chats:
                    self.bot.send_message(
                        chat_id, text,
                        parse_mode='HTML',
                        disable_web_page_preview=True)
            else:
                logging.info('{} Times {}'.format(e, self.error_times[url]))

    def send(self, entries, chats):
        for entry in entries:
            text = '<a href="{}">{}</a>'.format(entry[1], entry[0])
            for chat_id in chats:
                try:
                    self.bot.send_message(
                        chat_id, text,
                        parse_mode='HTML',
                        disable_web_page_preview=True)
                except (BadRequest, Unauthorized):
                    self.rss_fetcher.database.delete_all_relation_by_id(
                        chat_id)
                except TimedOut:
                    logging.error('send message timedout')

    def broadcast(self, entries, url):
        if not self.rss_fetcher.database.find_push(url):
            return

        for entry in entries:
            text = '<a href="{}">{}</a>'.format(entry[1], entry[0])

            self.bot.send_message(
                "@rssbotchannel",
                text,
                parse_mode='HTML',
                disable_web_page_preview=True)

    def error(self, bot, update, error):
        try:
            raise error
        except BaseException as e:
            logging.error(e)

    def run(self):
        self.dispatcher.add_handler(CommandHandler('start', start))
        self.dispatcher.add_handler(CommandHandler('sub', self.subscribe))
        self.dispatcher.add_handler(CommandHandler('unsub', self.unsubscribe))
        self.dispatcher.add_handler(CommandHandler('rss', self.rss))
        self.dispatcher.add_handler(CommandHandler('all', self.all))
        self.dispatcher.add_handler(CommandHandler('push', self.push))
        self.dispatcher.add_error_handler(self.error)
        self.updater.start_polling()
