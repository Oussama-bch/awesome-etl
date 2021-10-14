import redis
import ast
from lib import get_creds, get_logger_module
from job import exec_etl_job
from datetime import datetime


def main():
    log = get_logger_module()
    log.info("Worker starts listening to Redis channel at : {}".format(
        str(datetime.now().isoformat())))
    redis_conn = get_creds("database.ini", "redis")
    subscriber = redis.Redis(
        host=redis_conn['host'], port=redis_conn['port'], db=redis_conn['db'])
    channel = redis_conn['channel']
    p = subscriber.pubsub()
    p.subscribe(channel)

    while True:
        message = p.get_message()
        if message and not message['data'] == 1:
            message = message['data'].decode('utf-8')
            log.info("Received message from Redis Channel : {}".format(message))
            exec_etl_job(message)


if __name__ == '__main__':
    main()
