import sys
import logging
from rss_bot import RSSBot
"""
获取参数启动Bot
"""
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    token = sys.argv[1]
    bot = RSSBot(token)
    bot.run()
