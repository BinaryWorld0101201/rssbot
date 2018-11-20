def start(bot, update):
    chat_id = update.message.chat_id
    text = '欢迎使用，玩的开心\n'
    text += '/rss 查看；/sub 订阅；/unsub 退订\n'
    text += '源码：<a href="https://github.com/nierunjie/rssbot">Github</a>，疯狂暗示小星星\n'
    text += '作者：@Lanthora\n'
    bot.send_message(chat_id, text,
                     parse_mode='HTML',
                     disable_web_page_preview=True)
