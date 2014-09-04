#!/usr/bin/env python
# encoding: utf-8
# author: zozoz

import datetime

import pika

def connection(submit_data):
    connect = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'
    ))
    channel = connect.channel()
    channel.queue_declare(queue='submit_queue1', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='submit_queue1',
        body=submit_data,
        properties=pika.BasicProperties(
            delivery_mode=2, # make message persistent
        )
    )
    connect.close()


def temporary():
    data = {
        'submissionid': 1,
        'label': 1000,
        'repo': 'Local',
        'language': 'GPP',
        'code': "#include<iostream>\nusing namespace std;\nint main(){"
                "int a,b;\nwhile(cin>>a>>b){cout<<a+b<<endl;}\n}",
        'testdataid': 1,
        'is_spj': False,
        'spj_type': '',
        'timelimit': 1000,
        'memorylimit': 65535,
        'datetime':datetime.datetime.now()
    }
    return repr(data)


if __name__ == '__main__':
    connection(temporary())
