import validators #publick class
import validate_types #my
# import random
import db
import config as cfg

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
    'URLs': {'https://i.ua', 'https://zz.co '},  #mandatory
    'max_time_for_url_retrive': 500, #optional, by default = 300 ms
    'max_exetute_time': 3600,  #optional, by default = 0 s = not restricted
    'max_depth': 4, #optional, by default = 4 s = not restricted
}

class Api:

    def __init__(self, URLs):
        # self.job_ID = get from DB
        for url in URLs:
            if validators.url(url):
                print(url)
            else:
                print('error URL ="{}"'.format(url))
        self.db  = db.DB(cfg.db['db_path'],cfg.db['db_name'])
        j_uuid  = self.db.db_add_job(len(URLs))
        print(j_uuid)


Api(URLs=request['URLs'])
