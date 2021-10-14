from lib import get_creds, get_database, get_object,  put_object, get_logger_module, load_to_postgres
import pandas as pd
from datetime import datetime, timezone


def exec_etl_job(job_id):
    
    log = get_logger_module()
    log.info("Start ETL job : {}".format(job_id))

    db_conn = get_creds("database.ini", "mongodb")
    dbname = get_database(db_conn['database'], db_conn['uri'])
    collection = dbname[db_conn['collection']]

    # value = object['jobId']
    object = get_object(collection, "jobId", job_id)
    object['jobStatus'] = "RUNNING"
    object['jobStartTime'] = str(datetime.now().isoformat())

    try:
        # 0- Update job status : RUNNING
        put_object(collection, "jobId", job_id,  object)

        # 1- Extract csv file
        df = pd.read_csv(object['fileLocation'])
        log.debug(df.shape)
        ingestion_date = str(datetime.now(timezone.utc).date())

        # 2 Transform : add technical columns
        df['job_date'] = ingestion_date
        df['job_id'] = job_id
        df['file_name'] = object['fileLocation']

        # 3 Load to postgres
        load_to_postgres(df)

        # 4- Update job status : COMPLETED
        object['jobStatus'] = "COMPLETED"
        object['jobEndTime'] = str(datetime.now(timezone.utc).isoformat())
        object['loadedLineCount'] = df.shape[0]
        put_object(collection, "jobId", job_id,  object)

    except BaseException as e:
        log.error(e)
        object['jobStatus'] = "ERROR"
        object['jobEndTime'] = str(datetime.now().isoformat())
        object['errorMessage'] = str(e)
        put_object(collection, "jobId", job_id,  object)
