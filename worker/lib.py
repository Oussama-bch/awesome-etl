import pymongo
import redis
from configparser import ConfigParser

# Get Mongo database


def get_database(DATABASE, URI):
    try:
        CONNECTION_STRING = URI
        client = pymongo.MongoClient(CONNECTION_STRING)
        return client[DATABASE]
    except BaseException as e:
        print(e)
# Update object in Mango collection

def put_object(collection, key, value,  object):
    try:
        query = {key: {"$eq": value}}
        object_to_update = collection.find_one(query)
        new_object = {'$set': object}
        collection.update_one(object_to_update, new_object)
    except BaseException as e:
        print(e)

# Get Mongo and Redis creds from local file


def get_creds(filename, section):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
    return db


def pub_msg_to_redis(message):

    try:

        redis_conn = get_creds("database.ini", "redis")
        publisher = redis.Redis(
            host=redis_conn['host'], port=redis_conn['port'], db=redis_conn['db'])
        channel = redis_conn['channel']
        send_message = "Published message is  : " + str(message)
        publisher.publish(channel, send_message)
    except BaseException as e:
        print(e)
