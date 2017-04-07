#!/usr/bin/python
# encoding: utf-8
import json
import os
import re
from os.path import join, dirname

from bs4 import BeautifulSoup
from dotenv import load_dotenv

import db
import event
import util

WEIXIN_HOST = 'http://mp.weixin.qq.com'

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

COOKIE = os.environ.get("COOKIE")


class Crawler:
    def __init__(self):
        self.host = 'http://mp.weixin.qq.com'

    def run(self):
        db.set_status(1)
        util.clear_log()
        util.log("current cookie : " + COOKIE)
        for source in db.source_list():
            util.log("source " + source['name'] + " started")
            url = "http://weixin.sogou.com/weixin?type=1&s_from=input&query=" + source['source'] + "&ie=utf8"

            # search result page
            profile_url = ''
            times = 0
            while True:
                if db.get_status() != 1:
                    util.log("stopped!")
                    db.set_status(0)
                    return

                # the cookie could be out of date
                res = util.request(url, {'Cookie': COOKIE})
                if res is None:
                    break

                soup = BeautifulSoup(res.text, 'lxml')
                profile = soup.select_one('.img-box a')
                if profile is not None:
                    profile_url = profile.attrs['href']
                    break
                times = util.sleep_and_open(url, 'verify search url', times)

            # news profile page
            data = {}
            times = 0
            while True:
                if db.get_status() != 1:
                    util.log("stopped!")
                    db.set_status(0)
                    return

                res = util.request(profile_url)
                if res is None:
                    break

                matches = re.findall(r'var msgList = (.*);', res.text)
                if len(matches) > 0:
                    data = json.loads(matches[0])
                    break
                times = util.sleep_and_open(profile_url, 'verify profile url', times)

            if len(data) > 0:
                self.save(data, source)

        event.after_crawler_finished()
        db.set_status(0)
        util.log("done!")

    def save(self, data, source):
        for row in data['list']:

            title, cover, published_at, news_id = self.extract(row)

            url = (WEIXIN_HOST + row['app_msg_ext_info']['content_url']).replace('amp;', '')
            file_name = util.md5(source['source'] + ' ' + str(news_id))

            file_path = dirname(__file__) + '/page/' + file_name + '.html'
            if os.path.exists(file_path):
                continue
            util.log("page hash : " + file_name)

            res = util.request(url)
            if res is None:
                continue

            content = res.text.encode('utf-8')
            page = open(file_path, 'w')
            page.write(content)

            event.after_news_saved(res, file_path, file_name, news_id, title, cover, published_at, source)
        event.after_source_finished(source)

    @staticmethod
    def extract(row):
        title = row['app_msg_ext_info']['title']
        cover = row['app_msg_ext_info']['cover']
        published_at = row['comm_msg_info']['datetime']
        news_id = row['comm_msg_info']['id']

        return title, cover, published_at, news_id
