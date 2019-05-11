import os
import sqlite3
import uuid
import config as cfg

# config = dict(db_path=os.path.join('.','db'),
#               db_name = 'crawler.sqlite',
#               project_name = 'PythonFans-crawler',
#               # db_version = '0.0.1'
#               )

sql_init_structure = """
    CREATE TABLE "jobs" (
        "Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "uuid"	TEXT UNIQUE,
        "URLs"	INTEGER,
        "Start_Date"	DATE DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now'))
    );
    
    CREATE TABLE "info" (
        "name"	TEXT,
        "value"	TEXT
    );
  
    CREATE TABLE "robots_txt" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"job_uuid"	TEXT,
	"domain"	TEXT,
	"result_codes"	TEXT,
	"value"	TEXT,
	"date"  DATE,
	"in_queue"	INTEGER 
);
"""

sql_init_populate_date = """
    INSERT INTO info  VALUES ('project', '{}') ;
    INSERT INTO info  VALUES ('db_create', strftime('%Y-%m-%d %H:%M:%S','now')) ;
""".format(cfg.db['project_name'])

sql_get_tables = """
    SELECT 
        name
    FROM 
        sqlite_master 
    WHERE 
        type ='table' AND 
        name NOT LIKE 'sqlite_%';
"""
sql_get_table_name = """
    SELECT 
        name
    FROM 
        sqlite_master 
    WHERE 
        type ='table' AND 
        name LIKE ?;
"""



class DB:

    def __init__(self, db_path = '.', db_name = 'test.sqlite'):
        if not os.path.exists(db_path):
            try:
                os.mkdir(db_path)
            except:
                return 'error crerate db_path dir {}'.format(db_path)
        self.db_full_path = os.path.join(db_path, db_name)
        try:
            self.conn = sqlite3.connect(self.db_full_path)
            self.cursor = self.conn.cursor()
        except:
            return 'cannot use DB file {}'.format(self.db_full_path)

        if self.db_check == False:
            self.db_init()

    @property
    def db_check(self):
        try:
            self.cursor.execute('SELECT * FROM info WHERE name="project"')
            res = self.cursor.fetchall()
            return res[0] == ('project', cfg.db['project_name'])
        except:
            return False


    def db_init(self):
        try:
            self.cursor.executescript(sql_init_structure)
            self.cursor.executescript(sql_init_populate_date)
            return True
        except:
            return False

    def db_add_job(self, URLs_count=0):
        try:
            sql = """INSERT INTO jobs VALUES ('project', '{}')""".format(cfg.db['project_name'])
            job_uuid = uuid.uuid4()
            self.conn.execute("INSERT INTO jobs (URLs, uuid) VALUES (?,?);",(URLs_count, str(job_uuid)))
            self.conn.commit()
            return job_uuid
        except:
            return False

    def __delete__(self, instance):
        self.conn.commit()
        self.conn.close()


# db  = DB(cfg.db['db_path'],cfg.db['db_name'])
# print(db.db_add_job(100))
