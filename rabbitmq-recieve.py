#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('docker.nslookup.pp.ua'))
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # time.sleep(body.count(b'.'))
    time.sleep(5)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # ch.basic_nack()


channel.basic_consume(
    # queue='hello', on_message_callback=callback, auto_ack=True)
    queue='hello', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.basic_qos(prefetch_count=1,prefetch_size=100)
# channel.basic_qos(prefetch_size=1000)
channel.start_consuming()