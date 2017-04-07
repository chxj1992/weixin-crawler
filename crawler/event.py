#!/usr/bin/python
# encoding: utf-8

import util


def after_news_saved(res, file_path, file_name, news_id, title, cover, published_at, source):
    util.log("news saved")


def after_source_finished(source):
    util.log("source " + source['name'] + " finished")


def after_crawler_finished():
    util.log("crawler finished")
