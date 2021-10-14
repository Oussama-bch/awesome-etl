import pymongo
import redis
from configparser import ConfigParser
from sqlalchemy import create_engine

import logging

# Logger


def get_logger_module():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


log = get_logger_module()

# Get Mongo database


def get_database(DATABASE, URI):
    try:
        CONNECTION_STRING = URI
        client = pymongo.MongoClient(CONNECTION_STRING)
        return client[DATABASE]
    except BaseException as e:
        log.error(e)

# Get one object from Mongo collection


def get_object(collection, key, value):
    try:
        res = collection.find_one({key: value}, {'_id': False})
        return (res)
    except BaseException as e:
        log.error(e)

# Update object in Mango collection


def put_object(collection, key, value,  object):
    try:
        query = {key: {"$eq": value}}
        object_to_update = collection.find_one(query)
        new_object = {'$set': object}
        collection.update_one(object_to_update, new_object)
    except BaseException as e:
        log.error(e)

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

# Insert data to postgres


def load_to_postgres(df):

    db_conn = get_creds("database.ini", "postgres")

    strdb = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            db_conn['username'], db_conn['password'], db_conn['host'], db_conn['port'], db_conn['database'])
    log.debug(strdb)
    try:
        engine = create_engine(strdb, client_encoding='UTF-8')
        with engine.connect() as conn, conn.begin():
            df.to_sql(db_conn['table'], engine,
                      if_exists='append', index=False, chunksize=1000)
    except BaseException as e:
        log.error(e)
