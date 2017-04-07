#!/usr/bin/python
# encoding: utf-8
from os.path import dirname

from tinydb import TinyDB, Query


def db():
    return TinyDB(dirname(__file__) + '/db.json')


def get_status():
    return 0 if len(db().search(Query().status == 1)) == 0 else 1


def set_status(status):
    if status == 1:
        db().insert({'status': 1})
    else:
        db().remove(Query().status == 1)


def config_table():
    return db().table('config')


def set_config(config):
    config_table().purge()
    config_table().insert(config)


def get_config():
    return {} if len(config_table().all()) == 0 else config_table().all()[0]


def source_table():
    return db().table('sources')


def add_source(source_id, source, name):
    delete_source(source_id)
    source_table().insert({'id': source_id, 'source': source, 'name': name})


def delete_source(source_id):
    source_table().remove(Query().id == source_id)


def update_source(source_id, source, name):
    source_table().update({'source': source, 'name': name}, Query().id == source_id)


def get_source(source_id):
    return source_table().get(Query().id == source_id)


def source_list():
    return sorted(source_table().all(), key=lambda source: source['id'], reverse=True)
