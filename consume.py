#!/usr/bin/env python
# encoding: utf-8
# author: zozoz

import datetime
import time

import pika

import config
from judge import judge


class Consumer(object):

    def __init__(self):
        self.parameters = pika.ConnectionParameters(host='localhost')
        self.connect = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'
            ))
        self.channel = self.connect.channel()
        self.channel.queue_declare(queue='submit_queue1', durable=True)

    def _write_source_code(self, submission):
        with open(config.lastSource, 'w') as fp:
            #fp.write("//requesttime: %s\n" % submission['datetime'])
            #fp.write("//submissionid: %s\n") % submission['submissionid']
            #fp.write("//language: %s\n" % submission['language'])
            #fp.write("//is_spj: %s\n" % submission['is_spj'])
            fp.write(submission['code'])

    def process(self, ch, method, props, body):
        tt = time.time()
        print "I am process."
        try:
            submission = eval(body)
        except Exception, e:
            config.logger.error(e)
            print body
        config.logger.info("已经获得判题请求.")
        if not submission['is_spj']:
            is_spj = False
            spj_lang = 0
        else:
            is_spj = True
            spj_lang = submission['spj_type']

        lang = submission['language']
        if lang == 'GCC':
            lang = config.LANG_C
        elif lang == 'GPP':
            lang = config.LANG_CPP
        elif lang == 'Java':
            lang = config.LANG_JAVA
        self._write_source_code(submission)
        config.logger.info("开始判题.")
        try:
            result = judge(config.lastSource, lang, submission['testdataid'],
                    submission['timelimit'], submission['memorylimit'], is_spj, spj_lang)
            result['submissionid'] = submission['submissionid']
            print 'lang: %s' % lang
        except Exception, e:
            config.logger.error(e)
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            config.logger.info("判题完成. %s" % result["status"])
            print time.time() - tt

    def start_consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.process, queue='submit_queue1')
        self.channel.start_consuming()
        print 'I am consume.'


