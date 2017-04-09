#!/usr/bin/python
# encoding: utf-8
import threading

from flask import Blueprint, request

from crawler import db, util
from crawler.crawler import Crawler

api = Blueprint('api', __name__)


@api.route("/crawl/log")
def crawl_log():
    return util.response(0, {'log': util.output_log(), 'status': db.get_status()})


@api.route("/crawl/status")
def crawl_status():
    return util.response(0, db.get_status())


@api.route("/crawl/stop")
def crawl_stop():
    db.set_status(0)
    return util.response(0, 'stopped')


@api.route("/crawl/start")
def crawl_start():
    if db.get_status() == 1:
        return util.response(1, 'crawler is running!')
    else:
        c = Crawler()
        t = threading.Thread(target=c.run)
        t.start()
        return util.response(0, 'started')


@api.route("/source/add")
def source_add():
    validate = util.validate(request.args, ['source', 'name'])
    if validate is not True:
        return util.response(1, 'params error : ' + validate)
    db.add_source(request.args['source'], request.args['name'])
    return util.response(0, 'source added')


@api.route("/source/remove")
def source_remove():
    validate = util.validate(request.args, ['source'])
    if validate is not True:
        return util.response(1, 'params error : ' + validate)
    db.delete_source(request.args['source'])
    return util.response(0, 'source removed')


@api.route("/source/update")
def source_update():
    validate = util.validate(request.args, ['source', 'name'])
    if validate is not True:
        return util.response(1, 'params error : ' + validate)
    db.update_source(request.args['source'], request.args['name'])
    return util.response(0, 'source updated')


@api.route("/source/list")
def source_list():
    return util.response(0, db.source_list())

