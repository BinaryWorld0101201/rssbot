# Telegram RSS Bot

## 功能
订阅与退订RSS，更新的文章发送到Telegram

## 构建
建议直接使用[RSSBot](https://t.me/PythonRssBot)，坚持自行构建请仔细阅读以下内容
### 方法1：直接使用二进制文件(仅Linux平台)
1. 下载[二进制文件](https://github.com/nierunjie/rssbot/releases/download/v1.0/rssbot)
1. 添加可执行权限
1. 以token作为参数运行

该版本在保证功能完整的情况下，尽可能缩减代码量，仅提供`sub`,`unsub`,`rss`指令

### 方法2：从源代码开始构建(不推荐)
1. 根据`rss.sql`中的指令新建名为`rss.db`的数据库(若存在请先删除)。
1. 将broadcast方法中的channel替换，若不需要在频道中推送，可在update中注释掉broadcast。
1. 将token作为参数启动Bot即可。
1. backup.sh为数据库备份脚本，请妥善使用

## 命令
|命令|解释|
|:-|:-|
|/rss|查看自己的订阅|
|/all|查看所有用户的订阅，在这里寻找感兴趣的内容|
|/sub|订阅，后跟带协议(http 或 https)的url，缺少协议将导致订阅失败|
|/unsub|退订，与订阅方式完全相同|
|/push|后跟url可设置是否推送到频道，不跟参数则显示已经推送到频道的RSS|

## 其他
[RSSHub](https://docs.rsshub.app/)万物皆可RSS，配合RSSBot可应对很多场景。

