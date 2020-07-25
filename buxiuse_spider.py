# -*- coding:utf8 -*-

import requests
import os
from bs4 import BeautifulSoup
import random
import pymysql
import time

se = requests.session()


class BuXiuSeSpider:

    def __init__(self):
        self.connect = pymysql.connect(
            host="localhost",
            user='root',
            passwd='root',
            db='spider',
            charset='utf8mb4'
        )
        self.cursor = self.connect.cursor()
        self.headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        }
        print("数据库连接成功")

    def parse(self, html):
        home_page_soup = BeautifulSoup(html, 'lxml')
        thumb_list = home_page_soup.findAll('li', class_="span3")
        for thumb in thumb_list:
            # 随机休眠1到5秒
            sleep = random.randint(1, 5)
            print("休息", sleep, "秒")
            time.sleep(sleep)
            self.parse_item(thumb)

    def parse_item(self, thumb):
        img = thumb.find('img', class_="height_min")
        title = img.get('title')
        title.encode('utf-8')
        title = title.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_').replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
        url = img.get('src')
        star = thumb.find('span', class_="starcount")
        star = star.get_text()
        self.insert(title, url, star)
        self.save_pic(title, url)

    def insert(self, title, url, star):
        insert_sql = """insert into buxiuse(id,title,url,star) values (null,%s,%s,%s)"""
        # 执行sql操作
        self.cursor.execute(
            insert_sql, (title, url, star)
        )
        # 提交sql操作
        self.connect.commit()

    def close_connect(self):
        # 先关闭游标再关闭连接
        self.cursor.close()
        self.connect.close()
        print("数据库连接已关闭")

    def save_pic(self, title, url):
        save_path = "F:\\buxiuse\\"+title+".jpg"
        bytes = se.get(url).content
        if os.path.exists(save_path):
            save_path = "F:\\buxiuse\\"+title+str(random.randint(0, 10))+".jpg"
        f = open(save_path, 'wb')
        f.write(bytes)
        f.flush()
        f.close()
        if os.path.exists(save_path):
            print(save_path, "->保存成功")
        else:
            print(save_path, "保存失败,递归保存")
            self.save_pic(title, url)

    def work(self):
        try:
            for page in range(1, 101):
                # 随机休眠1到5秒
                sleep = random.randint(1, 5)
                print("休息", sleep, "秒")
                time.sleep(sleep)
                url = 'https://www.buxiuse.com/?page=%s' % page
                html = se.get(url, headers=self.headers).text
                self.parse(html)
        except RuntimeError as error:
            print(error)

        # 关闭数据库连接
        self.close_connect()


bxs = BuXiuSeSpider()
bxs.work()