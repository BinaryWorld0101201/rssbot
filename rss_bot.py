from telegram.ext import Updater, Job, CommandHandler
from rss_fetcher import RSSFetcher
from telegram import Bot
from datetime import datetime


class RSSBot(object):
    def __init__(self, token):
        self.bot = Bot(token)
        self.rss_fetcher = RSSFetcher()
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.updater.job_queue.run_repeating(self.refresh, 300)
        self.updater.job_queue.start()

    def subscribe(self, bot, update):
        chat_id = update.message.chat_id
        try:
            url = update.message.text.split(' ')[1]
            ret = self.rss_fetcher.subscribe(url, chat_id)
            text = ret and '订阅成功' or '订阅失败'
        except IndexError:
            text = '请输入正确的格式\n/sub 订阅的URL'
        bot.send_message(chat_id, text)

    def unsubscribe(self, bot, update):
        chat_id = update.message.chat_id
        url = update.message.text.split(' ')[1]
        self.rss_fetcher.unsubscribe(url, chat_id)
        text = '该订阅已成功取消'
        bot.send_message(chat_id, text)

    def list(self, bot, update):
        chat_id = update.message.chat_id
        text = self.rss_fetcher.list(chat_id)
        bot.send_message(chat_id, text)

    def refresh(self, bot, job):
        urls = self.rss_fetcher.find_all_urls_and_time()
        for url in urls:
            time = datetime.fromisoformat(urls.get(url))
            entries = self.rss_fetcher.get_entries_after_time(url, time)
            chats = self.rss_fetcher.find_chats_by_url(url)
            self.send(entries, chats)

    def send(self, entries, chats):
        for entry in entries:
            text = '[{}]({})'.format(entry[0], entry[1])
            for chat_id in chats:
                self.bot.send_message(
                    chat_id, text,
                    parse_mode='Markdown',
                    disable_web_page_preview=True)

    def error(self, bot, update, error):
        try:
            raise error
        except:
            print(error)

    def run(self):
        self.dispatcher.add_handler(CommandHandler('sub', self.subscribe))
        self.dispatcher.add_handler(CommandHandler('unsub', self.unsubscribe))
        self.dispatcher.add_handler(CommandHandler('list', self.list))
        self.dispatcher.add_error_handler(self.error)
        self.updater.start_polling()
