import config as cfg
import pika

#!/usr/bin/env python
import pika
import time
import datetime
import json


class RabbitMQ():

    def __init__(self,login='guest', password='guest', host='localhost', port=5672, vhost = '/', erase_on_connect=True):
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.vhost = vhost
        self.erase_on_connect = erase_on_connect

    def connect(self):
        credentials = pika.PlainCredentials(self.login, self.password, erase_on_connect=self.erase_on_connect)
        parameters = pika.ConnectionParameters(self.host, self.port, self.vhost, credentials)
        try:
            self.connection = pika.BlockingConnection(parameters)
        except Exception as error:
            return str(error)

        self.channel = self.connection.channel()


    def __del__(self):
        self.connection.close()

    def publish(self, body='',queue='hello',exchange='',routing_key=''):
        routing_key = routing_key or queue
        self.channel.queue_declare(queue=queue)

        # properties = pika.BasicProperties(delivery_mode=2)  # make message persistent
        properties = pika.BasicProperties(expiration=str(3600*1000))  # message age in ms
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body,properties=properties)

    def consume(self):
        self.channel.basic_consume(queue='hello',
                              auto_ack=True,
                              on_message_callback=self.callback)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)




def example():
    z = RabbitMQ(host='docker.nslookup.pp.ua')
    z.connect()
    rabbitmq_cfg = {'login': 'guest', 'password': 'guest', 'host': 'docker.nslookup.pp.ua',
                    'port': 5672}
    # z.publish(body=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    # z.publish(body='111111',queue='aaa')
    for i in range(100):
        z.publish(queue='hello',body=str(i) + '==' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
        z.publish(queue='hello',body=json.dumps(rabbitmq_cfg))
        # z.publish(body='zzz')
    # print(z)
    # del z
    pass

    # z.consume()
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # z.channel.start_consuming()


    # while True:
    #     z.publish(queue='hello',body='test')

