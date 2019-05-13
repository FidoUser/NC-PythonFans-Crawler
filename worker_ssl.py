#!/usr/bin/env python
import rabbitMQ
import config as cfg
import requests
import json
import db as DB
import ssl
# from cryptography import x509
# from cryptography.hazmat.backends import default_backend
import pem
import os



def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())

    try:
        msg = json.loads(body.decode())
    except:
        print('error decode message {}'.format(body.decode()))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return False, 'error decode message {}'.format(body.decode())

    try:
        cert_raw = ssl.get_server_certificate((msg['domain'], cfg.worker['https_port']))
        # cert_decode = x509.load_pem_x509_certificate(cert_raw, default_backend())
        cert_decode = pem.parse(cert_raw)
        db.cert_set_responce(domain=msg['domain'], cert_raw=cert_raw, cert_decode=cert_decode)
    except Exception as error:
        print('error ' + str(error))

    # pass
    # print(response.status_code)
    # print(response.text)

    # ssl.match_hostname(cert, hostname)   !!! check cert is valid for domain

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # ch.basic_nack()


rabbit = rabbitMQ.RabbitMQ(host=cfg.rabbit['docker_host'])
rabbit.connect()
# rabbit.channel.queue_declare(queue=cfg.rabbit['queue_ssl'])

db = DB.DB(cfg.db['db_path'], cfg.db['db_name'])



rabbit.channel.basic_consume(
    # queue='hello', on_message_callback=callback, auto_ack=True)
    queue=cfg.rabbit['queue_ssl'], on_message_callback=callback)

print("Current File Name : ",os.path.realpath(__file__))
print(' [*] Waiting for messages. To exit press CTRL+C')
rabbit.channel.start_consuming()


