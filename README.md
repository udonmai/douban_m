##本地mp3文件tag信息更正与豆瓣电台加心音乐下载

###简介

该工具分为两块，一块通过豆瓣音乐修正mp3文件的tag信息，利用[eyeD3](http://eyed3.nicfit.net/)来完成tag信息的读写。

另一块则是豆瓣电台的加心歌曲的下载，通过把握豆瓣后端存储服务器向前端输送歌曲文件的链接来获取文件名匹配成功的mp3文件。
HTML Parser是[Beautifulsoup](http://www.crummy.com/software/BeautifulSoup/)。

>图形界面采用[wxpython](http://wxpython.org/)，但是远未成型。

>下载不是太稳定，特别是设定了多个线程同时启动之后

[项目原始地址](https://github.com/icys13/douban/)
