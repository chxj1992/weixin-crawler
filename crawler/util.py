#!/usr/bin/python
# encoding: utf-8
import datetime
import hashlib
import json
import time
import webbrowser
from os.path import dirname

import qiniu
import requests
from flask import Response


def md5(url):
    return hashlib.md5(url).hexdigest()


def to_timestamp(time_str, time_format):
    try:
        return time.mktime(datetime.datetime.strptime(time_str, time_format).timetuple())
    except:
        return 0


def to_datetime(timestamp, date_format=False):
    date_format = date_format if date_format else '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.fromtimestamp(timestamp).strftime(date_format)


def sleep_and_open(url, msg='', times=0):
    log(msg + " sleep 5 seconds ...")
    if times % 6 == 0:
        webbrowser.open_new(url)
    time.sleep(5)
    return times + 1


def fetch_by_qiniu(url, bucket, name, ak, sk):
    try:
        q = qiniu.Auth(ak, sk)
        bucket_manager = qiniu.BucketManager(q)
        ret, info = bucket_manager.fetch(url.encode('utf-8'), bucket, name)
        if ret and 'key' in ret:
            return True
        else:
            return False
    except Exception as e:
        log(e, 'ERROR')
        return False


def clear_log(filename="crawl"):
    f = open(dirname(__file__) + "/log/" + filename + ".log", 'w')
    f.write("")
    f.close()


def log(content, level="INFO", filename="crawl"):
    f = open(dirname(__file__) + "/log/" + filename + ".log", 'a')
    f.write("[" + level + "] [" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " +
            content.encode('utf-8') + "\n")
    f.close()


def output_log(filename="crawl"):
    with open(dirname(__file__) + "/log/" + filename + ".log", 'r') as content:
        return content.read()


def response(code, data):
    return Response(json.dumps({'code': code, 'data': data}))


def validate(params, fields):
    for field in fields:
        if field not in params.keys() or params[field] == '':
            return field
    return True


def request(url, headers=None):
    try:
        res = requests.get(url, headers=headers)
    except Exception as e:
        log("page network error!" + str(e), 'ERROR')
        return None
    if res.status_code != 200:
        log('page status error : ' + str(res.status_code) + ' ' + url, 'ERROR')
        return None
    return res
