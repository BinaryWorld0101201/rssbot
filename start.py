def start(bot, update):
    chat_id = update.message.chat_id
    text = '欢迎使用，玩的开心\n\n'
    text += '/all 查看所有用户的订阅，在这里寻找感兴趣的内容\n'
    text += '/rss 查看自己的订阅，此处订阅会进行推送\n'
    text += '/sub 订阅，后跟带协议(http 或 https)的url，缺少协议将导致订阅失败\n'
    text += '/unsub 退订，与订阅方式完全相同\n\n'

    text += '源码：<a href="https://github.com/nierunjie/rssbot">GitHub</a>\n'
    text += '作者：@Lanthora\n'
    bot.send_message(chat_id, text,
                     parse_mode='HTML',
                     disable_web_page_preview=True)
