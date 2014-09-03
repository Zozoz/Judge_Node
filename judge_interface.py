import pika

class Consumer(object):

    def __init__(self):
        self.parameters = pika.ConnectionParameters(host='localhost')
        self.connect = pika.BlockingConnection(self.parameters)
        self.channel = self.connect.channel()
        self.channel.queue_declare(queue='submit_queue', durable=True)

    def process(self, ch, method, props, body):
        submit_data = eval(repr(body))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.process, queue='submit_queue')
        self.channel.start_consuming()


if __name__ == '__main__':
    consume = Consumer()