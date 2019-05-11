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