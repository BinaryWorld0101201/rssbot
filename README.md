# Telegram RSS Bot

## 功能
订阅与退订RSS，更新的文章发送到Telegram

## 运行
根据`rss.sql`中的指令新建名为`rss.db`的数据库(若存在请先删除)。将token作为参数启动Bot即可。

## Bot
[RSSBot](https://t.me/PythonRssBot)

|命令|解释|
|:-|:-:|
|/rss|查看自己的订阅|
|/all|查看所有用户的订阅，在这里寻找感兴趣的内容|
|/sub|订阅，后跟带协议(http 或 https)的url，缺少协议将导致订阅失败|
|/unsub|退订，与订阅方式完全相同|
|/push|后跟url可设置是否推送到频道，不跟参数则显示已经设置推动到频道的RSS|

### 订阅
* Github
```
/sub https://github.com/nierunjie/rssbot/commits/master.atom
```
* 微博
在[此处](https://api.izgq.net/weibo/)生成新浪微博RSS链接
