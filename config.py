import os

api = dict(
    max_time_for_url_retrive= 5000,
    max_exetute_time = 3600,
)

db = dict(
    db_path=os.path.join('.', 'db'),
    db_name='crawler.sqlite',
    project_name='PythonFans-crawler',
    # db_version = '0.0.1'
)

rabbit = dict(
    docker_host='docker.nslookup.pp.ua',
    queue_robots_txt = 'robots.txt',
    queue_ssl = 'ssl',
    queue_urls = 'URLs',
)

worker = dict(
    request_ConnectTimeout = 500, #ms
    request_ReadTimeout = 10, #sec
    https_port = 443
)


request = {
    'URLs': {'https://i.ua', 'https://zz.co ', 'https://www.namecheap.com'},  #mandatory
    'max_ConnectTimeout': 500, #optional, by default = 300 ms (ConnectTimeout)
    'max_ReadTimeout': 10, #optional, by default = 10 sec
    'max_exetute_time': 3600,  #optional, by default = 0 s = not restricted
    'max_depth': 4, #optional, by default = 4 s = not restricted
}
