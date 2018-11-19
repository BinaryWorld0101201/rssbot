def start(bot, update):
    chat_id = update.message.chat_id
    text = '欢迎使用，希望你玩的开心\n'
    text += '作者：@Lanthora\n'
    text += '在<a href="https://github.com/nierunjie/rssbot">Github</a>查看源码\n'
    text += '疯狂暗示小星星\n'
    bot.send_message(chat_id, text,
                     parse_mode='HTML',
                     disable_web_page_preview=True)
