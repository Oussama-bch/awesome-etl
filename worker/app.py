import redis
import ast
from lib import get_creds
from etl_job import exec_etl_job
from time import sleep

def main():
    redis_conn = get_creds("database.ini", "redis")
    subscriber = redis.Redis(
        host=redis_conn['host'], port=redis_conn['port'], db=redis_conn['db'])
    channel = redis_conn['channel']
    p = subscriber.pubsub()
    p.subscribe(channel)

    while True:
        sleep(2)
        message = p.get_message()
        if message and not message['data'] == 1:
            message = message['data'].decode('utf-8')
            print(message)
            exec_etl_job(ast.literal_eval(message))

if __name__ == '__main__':
    main()
