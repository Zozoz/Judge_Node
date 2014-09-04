#!/usr/bin/env python
# encoding: utf-8
# authot: zozoz

import os

import config
from consume import Consumer

def _init():
    if not os.path.isdir(config.data_dir):
        os.mkdir(config.data_dir)
    if not os.path.isdir(config.run_dir):
        os.mkdir(config.run_dir)
    with open(config.lastSource, 'a'):
        os.utime(config.lastSource, None)

def work():
    consume = Consumer()
    consume.start_consume()


if __name__ == '__main__':
    _init()
    while True:
        try:
            work()
        except Exception, e:
            config.logger.error(e)
