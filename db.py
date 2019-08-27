import os
import sqlite3
import uuid
import config as cfg
import inspect
import sys

# config = dict(db_path=os.path.join('.','db'),
#               db_name = 'crawler.sqlite',
#               project_name = 'PythonFans-crawler',
#               # db_version = '0.0.1'
#               )


datetime_msg = dict (datetime = """datetime("now","localtime")""",
                     strftime = """strftime('%Y-%m-%d %H:%M:%S','now', 'localtime')"""
                     )

sql_init_structure = """
    CREATE TABLE "jobs" (
        "Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "uuid"	TEXT UNIQUE,
        "URLs"	INTEGER,
        -- "Start_Date"	DATE DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now')),  -- GMT
        -- "Start_Date"	DATE DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime')),  -- GMT
        "Start_Date"	DATE DEFAULT (-=-datetime-=-)  -- local timezone
        
    );
    
    CREATE TABLE "info" (
        "name"	TEXT,
        "value"	TEXT
    );
  
    CREATE TABLE "robots_txt" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"job_id"	INTEGER,
	"domain"	TEXT,
	"result_code"	TEXT,
	"value"	TEXT,
	"last_update"  DATE,
	"in_queue"	INTEGER 
    );
    
    CREATE TABLE "ssl" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"job_id"	INTEGER,
	"domain"	TEXT,
	"result_codes"	TEXT,
	"cert"	TEXT,
	"cert_raw"	TEXT,
	"last_update"  DATE,
	"in_queue"	INTEGER 
    );
    
    CREATE TABLE "URLs" (
	"Id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"job_id"	INTEGER,
	"domain"	TEXT,
	"url"	TEXT,
	"depth"	INTEGER,
	"max_depth"	INTEGER,
	"result_code"	TEXT,
	"html"	TEXT,
	"last_update"	DATE,
	"in_queue"	INTEGER
    );
""".replace('-=-datetime-=-', datetime_msg['strftime'])

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

    def __init__(self, db_path='.', db_name='test.sqlite'):
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

    def add_job(self, URLs_count=0):
        try:
            # sql = """INSERT INTO jobs VALUES ('project', '{}')""".format(cfg.db['project_name'])
            job_uuid = str(uuid.uuid4())
            self.conn.execute("INSERT INTO jobs (URLs, uuid) VALUES (?,?);", (URLs_count, job_uuid))
            self.conn.commit()
            return job_uuid
        except Exception as e:
            return False, inspect.stack()[0][3], inspect.currentframe().f_code.co_name, sys._getframe().f_code.co_name, e

    def __delete__(self, instance):
        self.conn.commit()
        self.conn.close()

    def get_job_id_from_uuid(self, job_uuid):
        try:
            # sql = """SELECT id from jobs WHERE uuid='{}'""".format(str(job_uuid))
            sql = """SELECT id from jobs WHERE uuid="?"; """.replace('?',job_uuid)
            res = self.conn.execute(sql)
            for row in res:
                return row[0]
        except Exception as e:
            return False, inspect.stack()[0][3], inspect.currentframe().f_code.co_name, sys._getframe().f_code.co_name, e

    def add_robots_txt(self, domain, force_update=False, job_id=-1):
        try:
            sql = """SELECT id from robots_txt WHERE domain="?"; """.replace('?',domain)
            res = self.conn.execute(sql)
            #check if domain already checked !!!

            # sql = """INSERT INTO robots_txt (job_id, domain, in_queue) VALUES (1,'i.ua',1); """
            sql = """INSERT OR REPLACE INTO robots_txt (id, job_id, domain, in_queue) VALUES 
                    ((SELECT id from robots_txt WHERE domain="{}"),{},"{}",1); 
                  """.format(domain,job_id,domain)
            self.conn.execute(sql)
            self.conn.commit()
        except:
            return False

    def robots_txt_set_responce(self,domain, result_code, value=''):
        try:
            sql = """INSERT OR REPLACE INTO robots_txt (id, job_id, domain, in_queue, last_update, result_code) VALUES 
                    ((SELECT id from robots_txt WHERE domain="{}"),
                    (SELECT job_id from robots_txt WHERE domain="{}"),
                    "{}",0, -=-datetime-=-, "{}" ); 
                  """.format(domain, domain, domain, str(result_code))\
                      .replace("-=-datetime-=-", datetime_msg['datetime'])
            self.conn.execute(sql)
            self.conn.commit()

            sql = """UPDATE robots_txt SET value="-=-value-=-" WHERE domain="{}" 
                  """.format(domain)\
                      .replace("-=-value-=-", value.replace('"','""'))
            self.conn.execute(sql)
            self.conn.commit()

        except:
            print('error sql robots_txt_set_responce')
            print(sql)
            return False


    def cert_set_responce(self, domain, cert_raw, cert_decode):
        try:
            sql = """INSERT OR REPLACE INTO ssl (id, job_id, domain, in_queue, last_update) VALUES 
                    ((SELECT id from robots_txt WHERE domain="{}"),
                    (SELECT job_id from robots_txt WHERE domain="{}"),
                    "{}",0, -=-datetime-=- ); 
                  """.format(domain, domain, domain)\
                      .replace("-=-datetime-=-", datetime_msg['datetime'])
            self.conn.execute(sql)
            self.conn.commit()

            sql = """UPDATE ssl SET cert_raw="-=-value-=-" WHERE domain="{}" 
                  """.format(domain)\
                      .replace("-=-value-=-", cert_raw.replace('"','""'))
            self.conn.execute(sql)
            self.conn.commit()

            sql = """UPDATE ssl SET cert_decode="-=-value-=-" WHERE domain="{}" 
                  """.format(domain)\
                      .replace("-=-value-=-", cert_decode.replace('"','""'))
            self.conn.execute(sql)
            self.conn.commit()

        except Exception as error:
            print('error in cert_set_responce = ' + error)
            print(sql)
            return False


    def add_ssl(self, domain, force_update=False, job_id=-1):
        try:
            sql = """SELECT id from ssl WHERE domain="?"; """.replace('?',domain)
            res = self.conn.execute(sql)
            #check if domain already checked !!!

            # sql = """INSERT INTO robots_txt (job_id, domain, in_queue) VALUES (1,'i.ua',1); """
            sql = """INSERT OR REPLACE INTO ssl (id, job_id, domain, in_queue) VALUES 
                    ((SELECT id from ssl WHERE domain="{}"),{},"{}",1); 
                  """.format(domain,job_id,domain)
            self.conn.execute(sql)
            self.conn.commit()
        except:
            return False


    def add_url(self, URL, job_id=-1, depth=1, max_depth=1):
        try:
            sql = """INSERT INTO URLs (job_id, url, depth, max_depth, in_queue) VALUES 
                    ("{}", "{}",{},{}, 1); 
                  """.format(job_id, URL, depth, max_depth)
            self.conn.execute(sql)
            self.conn.commit()
        except:
            return False



# db  = DB(cfg.db['db_path'],cfg.db['db_name'])
# print(db.db_add_job(100))
