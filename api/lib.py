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

# Get one object from Mongo collection
def get_object(collection, key, value):
    try:
        res = collection.find_one({key: value}, {'_id': False})
        return (res)
    except BaseException as e:
        print(e)

# Create new object in Mongo Collection
def post_object(collection, object):
    try:
        collection.insert_one(object)
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


# Publish message into Redis channel
def pub_msg_to_redis(message):

    try:
        redis_conn = get_creds("database.ini", "redis")
        publisher = redis.Redis(
            host=redis_conn['host'], port=redis_conn['port'], db=redis_conn['db'])
        channel = redis_conn['channel']
        publisher.publish(channel, str(message))
    except RecursionError as e:
        print(e)
