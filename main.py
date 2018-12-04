import logging
import sys

from rss_bot import RSSBot

"""
获取参数启动Bot
"""
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

if __name__ == '__main__':
    logging.info('rssbot started')
    token = sys.argv[1]
    bot = RSSBot(token)
    bot.run()
