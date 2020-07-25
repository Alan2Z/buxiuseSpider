# 本脚本用来少量爬取不羞涩（https://www.buxiuse.com/）网站上的妹子图片

使用requests和bs4
使用mysql数据库存储爬取成功的图片信息
图片下载路径 F:\\buxiuse\\
如果你的机器上没有安装MySQL数据库，请注释掉和数据库相关的操作
运行
切换目录到脚本的存放路径 在cmd中输入
`python buxiuse_spider.py`

本脚本没有做ip池和UA池维护，因此很容易被目标网站的服务器识别为爬虫
