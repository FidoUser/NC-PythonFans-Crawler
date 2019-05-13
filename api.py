import validators #publick class
import validate_types #my
# import random
import db
import rabbitMQ
import config as cfg
import datetime
import json

def description():
    pass
    # получить список сайтов
    # запросить из них robots.txt
    # запросить SSL
    # отправляет иниформацию в DB and Rabbit
    #
    # request
    # {
    #     'URLs': {'url1', 'url2'},  #mandatory
    #     'max_time_for_url_retrive': 500, #optional, by default = 300 ms
    #     'max_exetute_time': 3600,  #optional, by default = 0 s = not restricted
    # }
    #
    #
    # response
    # {
    #     'URL1':  #exmaple namecheap.com
    #         {
    #             'tags':{
    #                 'title': 'tile of page',
    #                 'meta': 'meta tag entry of page',
    #                 'description': 'description tag of page'
    #             },
    #             'text_page': 'full text of html page',
    #             'internal_links': {'link1', 'link2'},
    #             'external_links': {'link1', 'link2'},
    #             'external_scripts': {'link1', 'link2'},
    #             'internal_images': {
    #                 id0: {'url':'url_to_image', 'image_title':'image title'},
    #                 id1: {'url':'url_to_image', 'image_title':'image title'}
    #             },
    #             'external_images': {
    #                 id0: {'url':'url_to_image', 'image_title':'image title'},
    #                 id1: {'url':'url_to_image', 'image_title':'image title'}
    #             },
    #         }
    # }
    #
    #
    # #=============
    #
    # #exmaple
    #
    # request
    # {
    #     'URLs': {'https://www.namecheap.com/', 'https://google.com/'}
    # }
    #
    # response
    # {
    #     'https://www.namecheap.com/':  #exmaple namecheap.com
    #         {
    #             'tags':{
    #                 'title': 'Cheap Domain Names - Buy Domain Names from $0.88 - Namecheap',
    #                 'meta': '<meta http-equiv="Content-type" content="text/html;charset=UTF-8">',
    #                 'description': 'Namecheap offers cheap domain names with the most reliable service. Buy domain names with Namecheap and see why over 2 million customers trust us with over 10 million domains!'
    #             }
    #             'text_page': 'full text of html page',
    #             'internal_links': {'link1', 'link2'},
    #             'external_links': {'link1', 'link2'},
    #             'external_scripts': {'https://cdn.cookielaw.org/consent/e6412ea3-29f7-41b5-b61e-e680161a7fd3.js', 'https://px.ads.linkedin.com/collect/?time=1550652810761&pid=Tag%20Linkedin&url=https%3A%2F%2Fwww.namecheap.com%2F&fmt=js&s=1'},
    #             'internal_images': {
    #                 id0: {'url':'url_to_image', 'image_title':'image title'},
    #                 id1: {'url':'url_to_image', 'image_title':'image title'}
    #             },
    #             'external_images': {
    #                 id0: {'url':'url_to_image', 'image_title':'image title'},
    #                 id1: {'url':'url_to_image', 'image_title':'image title'}
    #             },
    #         }
    # }

request = {
    'URLs': {'https://i.ua', 'https://zz.co ', 'https://www.namecheap.com'},  #mandatory
    'max_time_for_url_retrive': 0.500, #optional, by default = 300 ms (ConnectTimeout)
    'max_ReadTimeout': 10, #optional, by default = 10 sec
    'max_exetute_time': 3600,  #optional, by default = 0 s = not restricted
    'max_depth': 4, #optional, by default = 4 s = not restricted
}

class Api:

    def __init__(self, db_path='.', db_name='db.sqlite'):
        self.db  = db.DB(db_path, db_name)
        self.rabbit = rabbitMQ.RabbitMQ(host=cfg.rabbit['docker_host'])
        self.rabbit.connect()
        self.rabbit.channel.queue_declare(queue=cfg.rabbit['queue_ssl'])
        self.rabbit.channel.queue_declare(queue=cfg.rabbit['queue_robots_txt'])


        # self.rabbit.publish(queue='hello',body='+++==' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

    def get_domain_from_url(self,url):
        try:
            return url.split("//")[-1].split("/")[0]
        except:
            return False

    def add_URLs(self, URLs, max_depth = 1):
        # self.job_ID = get from DB

        j_uuid  = self.db.add_job(len(URLs))
        j_id = self.db.get_job_id_from_uuid(j_uuid)
        for url in URLs:
            if validators.url(url):
                # print(url)
                message = dict(domain=self.get_domain_from_url(url),
                               ConnectTimeout = request['max_time_for_url_retrive'] or cfg.request['max_ConnectTimeout'],
                               ReadTimeout = request['max_ReadTimeout'] or cfg.request['max_ReadTimeout']
                               )
                message = json.dumps(message)

                self.db.add_robots_txt(domain=self.get_domain_from_url(url), job_id=j_id)
                self.rabbit.publish(queue=cfg.rabbit['queue_robots_txt'],body=message)

                self.db.add_ssl(domain=self.get_domain_from_url(url), job_id=j_id)
                self.rabbit.publish(queue=cfg.rabbit['queue_ssl'],body=message)
            else:
                print('error URL ="{}"'.format(url))

        print(j_uuid)
        print(j_id)



api = Api(cfg.db['db_path'],cfg.db['db_name'])
api.add_URLs(URLs=request['URLs'], max_depth=request['max_depth'])


