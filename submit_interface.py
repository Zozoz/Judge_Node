import pika

def connection(submit_data):
    connect = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'
    ))
    channel = connect.channel()
    channel.queue_declare(queue='submit_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='',
        body=submit_data,
        properties=pika.BasicProperties(
            delivery_mode=2, # make message persistent
        )
    )
    connect.close()


def temporary():
    data = {
        'id': 1,
        'label': 1000,
        'repo': 'Local',
        'language': 'G++',
        'code': "#include<iostream>\nusing namespace std;\nint main(){"
                "int a,b;\nwhile(cin>>a>>b){cout<<a+b<<endl;}\n}",
        'testdataid': 1,
        'is_spj': False
    }
    return repr(data)

if __name__ == '__main__':
    submit_data = temporary()
    connection(submit_data)