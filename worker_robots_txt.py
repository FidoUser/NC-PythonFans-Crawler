#!/usr/bin/env python
import rabbitMQ
import config as cfg
import time
import requests
import json
import db as DB



def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    # time.sleep(body.count(b'.'))
    # time.sleep(5)

    try:
        msg = json.loads(body.decode())
    except:
        print('error decode message {}'.format(body.decode()))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return False, 'error decode message {}'.format(body.decode())

    try:
        response = requests.get("https://" + msg['domain'] + "/robots.txt",
                                timeout=(msg['ConnectTimeout'], msg['ReadTimeout']))
        db.robots_txt_set_responce(domain=msg['domain'], result_code=response.status_code, value=response.text)
    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')

    pass
    print(response.status_code)
    # print(response.text)


    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # ch.basic_nack()


rabbit = rabbitMQ.RabbitMQ(host=cfg.rabbit['docker_host'])
rabbit.connect()
rabbit.channel.queue_declare(queue=cfg.rabbit['queue_robots_txt'])

db = DB.DB(cfg.db['db_path'], cfg.db['db_name'])



rabbit.channel.basic_consume(
    # queue='hello', on_message_callback=callback, auto_ack=True)
    queue=cfg.rabbit['queue_robots_txt'], on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.basic_qos(prefetch_count=1,prefetch_size=100)
# channel.basic_qos(prefetch_size=1000)
rabbit.channel.start_consuming()


