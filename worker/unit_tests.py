from unittest import TestCase

from lib import get_creds, get_object, get_database, put_object


class unitTest(TestCase):
    def test_get_mongo_creds(self):
        self.assertEqual({'uri': 'mongodb://192.168.33.34:2717', 'database': 'etl', 'collection': 'jobs'},
                         get_creds("database.ini", "mongodb"))

    def test_get_redis_creds(self):
        self.assertEqual({'host': '192.168.33.34', 'port': '6379', 'db': '0', 'channel': 'etl_jobs'},
                         get_creds("database.ini", "redis"))

    def test_put_mango_object(self):
        self.assertEqual(None,
                         put_object(get_database(get_creds("database.ini", "mongodb")['database'], get_creds("database.ini", "mongodb")['uri'])[get_creds("database.ini", "mongodb")['collection']], "jobId", "xid1234", {"jobId": "xid1234", "jobStatus": "RUNNING"}))

    def test_get_mango_object(self):
        self.assertEqual({'jobId': 'xid1234', 'jobStatus': 'RUNNING'},
                         get_object(get_database(get_creds("database.ini", "mongodb")['database'], get_creds("database.ini", "mongodb")['uri'])[get_creds("database.ini", "mongodb")['collection']], "jobId", "xid1234"))
