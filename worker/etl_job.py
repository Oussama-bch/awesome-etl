from lib import get_creds, get_database, put_object

import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime


def exec_etl_job(object):

    db_conn = get_creds("database.ini", "mongodb")
    dbname = get_database(db_conn['database'], db_conn['uri'])
    collection = dbname[db_conn['collection']]
    value = object['jobId']
    object['jobStatus'] = "RUNNING"

    try:
        # Update job status : RUNNING
        put_object(collection, "jobId", value,  object)

        # Run ETL job
        exec(object['fileLocation'], object['jobId'])

        # Update job status : COMPLETED
        object['jobStatus'] = "COMPLETED"
        put_object(collection, "jobId", value,  object)

    except BaseException as e:
        print(e)
        object['jobStatus'] = "ERROR"
        put_object(collection, "jobId", value,  object)



def exec(path, uuid):
    db_conn = get_creds("database.ini", "postgres")

    try:
        # 1 extract csv file -> pandas dataframe
        df = pd.read_csv(path)
        print(df.shape)
        ingestion_date = str(datetime.now().date())

        # 2 Transform : add technical columns
        df['job_date'] = ingestion_date
        df['job_id'] = uuid
        df['file_name'] = path

        # 3 Load to postgres
        strdb = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            db_conn['username'], db_conn['password'], db_conn['host'], db_conn['port'], db_conn['database'])
        engine = create_engine(strdb, client_encoding='UTF-8')
        with engine.connect() as conn, conn.begin():
            df.to_sql(db_conn['table'], engine,
                      if_exists='append', index=False, chunksize=1000)
    except BaseException as e:
        print(e)