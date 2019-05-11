#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='docker.nslookup.pp.ua'))
channel = connection.channel()

# channel.queue_declare(queue='task_queue', durable=True)
channel.queue_declare(queue='task_queue')
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(5)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

pass

channel.basic_qos(prefetch_count=65535)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()