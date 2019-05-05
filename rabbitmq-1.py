#!/usr/bin/env python
import pika
import time
import datetime

rabbitmq_cfg = {'login':'guest', 'password':'guest', 'host': 'docker.nslookup.pp.ua',
                'port': 5672}
# connection = pika.BlockingConnection(pika.ConnectionParameters('docker.nslookup.pp.ua'))
# channel = connection.channel()

# credentials = pika.PlainCredentials('guest', 'guest')

def old():
    credentials = pika.PlainCredentials(rabbitmq_cfg['login'], rabbitmq_cfg['password'], erase_on_connect=True)
    parameters = pika.ConnectionParameters(rabbitmq_cfg['host'], rabbitmq_cfg['port'],
                                           '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # channel.queue_declare(queue='hello11',exclusive=True)
    channel.queue_declare(queue='hello')
    # zz = channel.queue_declare('',exclusive=True)
    for i in range(100):
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=str(i))
        time.sleep(0.3)
        channel.queue_declare(queue='hello11', exclusive=True)
        # channel.queue_declare(queue='', exclusive=True, auto_delete=True)
    print(" [x] Sent 'Hello World!'")
    connection.close()



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


    # def __new__(cls, *args, **kwargs):
    #
    #     credentials = pika.PlainCredentials(cls.login, cls.password, erase_on_connect=cls.erase_on_connect)
    #     parameters = pika.ConnectionParameters(cls.host, cls.port, cls.vhost, credentials)
    #     # credentials = pika.PlainCredentials(login, password, erase_on_connect=erase_on_connect)
    #     # parameters = pika.ConnectionParameters(host, port, vhost, credentials)
    #     try:
    #         cls.connection = pika.BlockingConnection(parameters)
    #     except Exception as error:
    #         return str('error')  #error to return in __init__
    #
    #     cls.channel = connection.channel()
    #     pass

    def __del__(self):
        self.connection.close()

    def publish(self, body='',queue='hello',exchange='',routing_key=''):
        routing_key = routing_key or queue
        self.channel.queue_declare(queue=queue)
        # self.channel.queue_bind(queue, exchange)

        properties = pika.BasicProperties(delivery_mode=2)  # make message persistent
        properties = pika.BasicProperties(expiration=str(3600*1000))  # make message persistent
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body,properties=properties)
        # self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=("-1-" + body), properties=properties)
        # self.channel.exchange_declare(exchange='logs', exchange_type='fanout')

        pass

    def consume(self):
        self.channel.basic_consume(queue='hello',
                              auto_ack=True,
                              on_message_callback=self.callback)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)




z = RabbitMQ(host='docker.nslookup.pp.ua')
z.connect()
# z.publish(body=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
# z.publish(body='111111',queue='aaa')
for i in range(100):
    z.publish(queue='hello',body=str(i) + '==' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    # z.publish(body='zzz')
# print(z)
# del z
pass

# z.consume()
# print(' [*] Waiting for messages. To exit press CTRL+C')
# z.channel.start_consuming()


while True:
    z.publish(queue='hello',body='test')

