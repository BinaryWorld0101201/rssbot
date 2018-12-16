def start(bot, update):
    chat_id = update.message.chat_id
    text = '欢迎使用，玩的开心\n\n'
    text += '/rss 自己的订阅，此处订阅会进行推送\n'
    text += '/sub 订阅，后跟带协议(http 或 https)的url，缺少协议将导致订阅失败\n'
    text += '/unsub 退订，使用方法同订阅\n'
    text += '/push 推荐到频道，使用方法同订阅\n\n'
    
    text += '源码：<a href="https://github.com/nierunjie/rssbot">GitHub ⭐</a>\n'
    text += '频道：<a href="https://t.me/rssbotchannel">RSS精选</a>\n'
    bot.send_message(chat_id, text,
                     parse_mode='HTML',
                     disable_web_page_preview=True)
