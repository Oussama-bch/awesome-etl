from unittest import TestCase

from lib import get_creds, get_object, get_database, post_object, pub_msg_to_redis


class unitTest(TestCase):
    def test_get_mongo_creds(self):
        self.assertEqual({'uri': 'mongodb://192.168.33.34:2717', 'database': 'etl', 'collection': 'jobs'},
                         get_creds("database.ini", "mongodb"))

    def test_get_redis_creds(self):
        self.assertEqual({'host': '192.168.33.34', 'port': '6379', 'db': '0', 'channel': 'etl_jobs'},
                         get_creds("database.ini", "redis"))

    def test_post_mango_object(self):
        self.assertEqual(None,
                         post_object(get_database(get_creds("database.ini", "mongodb")['database'], get_creds("database.ini", "mongodb")['uri'])[get_creds("database.ini", "mongodb")['collection']], {"jobId": "xid1234"}))

    def test_get_mango_object(self):
        self.assertEqual({'jobId': 'xid1234'},
                         get_object(get_database(get_creds("database.ini", "mongodb")['database'], get_creds("database.ini", "mongodb")['uri'])[get_creds("database.ini", "mongodb")['collection']], "jobId", "xid1234"))

    def test_pub_to_redis(self):
        self.assertEqual(None,
                         pub_msg_to_redis("helloworld"))
