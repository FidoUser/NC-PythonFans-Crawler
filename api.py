import validators #publick class
import validate_types #my
# import random
import db
import rabbitMQ
import config as cfg
import datetime
import json

from flask import Flask, request

app = Flask(__name__)
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

request1 = {
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

    def add_URLs(self, URLs, max_depth = 1, max_time_for_url_retrive = 0.5, max_ReadTimeout =10 ):
        # self.job_ID = get from DB

        j_uuid  = self.db.add_job(len(URLs))
        j_id = self.db.get_job_id_from_uuid(j_uuid)
        for url in URLs:
            if validators.url(url):
                # print(url)
                message = dict(domain=self.get_domain_from_url(url),
                               # ConnectTimeout = request1['max_time_for_url_retrive'] or cfg.request['max_ConnectTimeout'],
                               # ReadTimeout = request1['max_ReadTimeout'] or cfg.request['max_ReadTimeout']
                               )
                message = json.dumps(message)

                self.db.add_robots_txt(domain=self.get_domain_from_url(url), job_id=j_id)
                self.rabbit.publish(queue=cfg.rabbit['queue_robots_txt'],body=message)

                self.db.add_ssl(domain=self.get_domain_from_url(url), job_id=j_id)
                self.rabbit.publish(queue=cfg.rabbit['queue_ssl'],body=message)

                self.db.add_url(URL=url, job_id=j_id, depth=1, max_depth =request1['max_depth'])
                self.rabbit.publish(queue=cfg.rabbit['queue_urls'],body=message)


            else:
                print('error URL ="{}"'.format(url))

        print(j_uuid)
        print(j_id)

@app.route('/debug', methods = ['GET', 'POST'])
def flask_debug_api():
    html ="""
        
        <html>
            <head>
            </head>
            <body>
                <script>
                    function send_data(){
                        // Sending and receiving data in JSON format using POST method
                        //
                        var xhr = new XMLHttpRequest();
                        var url = "/api/request";
                        xhr.open("POST", url, true);
                        xhr.setRequestHeader("Content-Type", "application/json");
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState === 4 && xhr.status === 200) {
                                var json = JSON.parse(xhr.responseText);
                                console.log(json.email + ", " + json.password);
                            }
                        };
                        var data = JSON.stringify({
                            'URLs': ['https://i.ua ', 'https://zz.co ', 'https://www.namecheap.com/', 'https://google.com.ua '],  // mandatory
                            'max_time_for_url_retrive': 0.500, // optional, by default = 300 ms (ConnectTimeout)
                            'max_ReadTimeout': 10, // optional, by default = 10 sec
                            'max_exetute_time': 3600,  // optional, by default = 0 s = not restricted
                            'max_depth': 4, // optional, by default = 4 s = not restricted
                        });
                        xhr.send(data);
                    }
        
                    function rabbit_delete_all_queues_items(){
                        // Sending and receiving data in JSON format using POST method
                        //
                        var xhr = new XMLHttpRequest();
                        var url = "/api/action/rabbit_delete_all_queues_items";
                        xhr.open("POST", url, true);
                        xhr.setRequestHeader("Content-Type", "application/json");
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState === 4 && xhr.status === 200) {
                                var json = JSON.parse(xhr.responseText);
                                console.log(json.email + ", " + json.password);
                            }
                        };
                        // var data = JSON.stringify({});                
                        xhr.send();
                    }
        
                </script>
                <form>
                    <button type="button" onclick="send_data()">send_data</button>
                    <button type="button" onclick="rabbit_delete_all_queues_items()">rabbit_delete_all_queues_items</button>
                </form>
            </body>
        </html>    
                
    """
    return html

@app.route('/api/action/<action>', methods=['GET', 'POST'])
def flask_actions(action):
    if action == 'rabbit_delete_all_queues_items':
        for queue in [cfg.rabbit[q] for q in cfg.rabbit.keys() if q.startswith('queue_')]:
            api.rabbit.purge_queue(queue)
    return "{}"

@app.route('/api/request', methods=['GET','POST'])
def flask_request_put():
    print(request.json)
    api.add_URLs(URLs=request.json['URLs'], max_depth=request.json['max_depth'])
    return "{}"


api = Api(cfg.db['db_path'],cfg.db['db_name'])
api.add_URLs(URLs=request1['URLs'], max_depth=request1['max_depth'])




if __name__ == '__main__':
    app.run(debug=True)