import argparse
import os
import uuid

from lib import get_creds, get_database, post_object, get_object, pub_msg_to_redis
from datetime import datetime
from flask import Flask, jsonify, request, make_response
from flask_json_schema import JsonSchema, JsonValidationError


app = Flask(__name__)

###########################################################################
# Default error responses
###########################################################################


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


############################################################################
# Heath check Endpoint
############################################################################


@app.route('/healthz', methods=['GET'])
def health_check():
    app.logger.info("Health check request")
    return jsonify({'Application': 'is healthy !'}), 200


schema = JsonSchema(app)
body_schema = {
    'type': 'object',
    'required': ['fileLocation'],
    'properties': {
        'fileLocation': {'type': 'string'}
    }
}


@app.errorhandler(JsonValidationError)
def validation_error(e):
    app.logger.error("Bad service contract : {}".format(e.errors))
    return jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]}), 400

############################################################################
# POST Job
############################################################################


@app.route('/etl/jobs/start', methods=['POST'])
@schema.validate(body_schema)
def post_job():
    app.logger.info(" POST /etl/start")
    message = request.get_json()
    app.logger.debug(message)

    content = message.get("fileLocation", "")

    if not (os.path.isfile(content)):
        app.logger.warn("File not found.")
        return make_response(jsonify({'error': "File not found. Please check fileLocation value"}), 400)

    db_conn = get_creds("database.ini", "mongodb")
    job_id = str(uuid.uuid4())
    job_start_time = str(datetime.now().isoformat())

    object = {
        "jobId": job_id,
        "jobStatus": "STARTING",
        "fileLocation": content,
        "jobStartTime": job_start_time
    }
    try:
        app.logger.info("Connecting to the Mongodb database...")
        dbname = get_database(db_conn['database'], db_conn['uri'])
        collection = dbname[db_conn['collection']]
        post_object(collection, object)
        app.logger.info("Database connection closed.")
        pub_msg_to_redis({
            "jobId": job_id,
            "jobStatus": "STARTING",
            "fileLocation": content,
            "jobStartTime": job_start_time
        })
        return jsonify({'success': True, 'jobId': job_id, 'jobStatus': 'STARTING'}), 201
    except(Exception) as error:
        app.logger.error(error)
        return '', 503


############################################################################
# GET Job
############################################################################


@app.route('/etl/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    app.logger.info(" GET /etl/jobs/{}".format(job_id))
    db_conn = get_creds("database.ini", "mongodb")
    try:
        app.logger.info("Connecting to the Mongodb database...")
        dbname = get_database(db_conn['database'], db_conn['uri'])
        collection = dbname[db_conn['collection']]

        db_result = get_object(collection, "jobId", job_id)

        if db_result is not None:
            app.logger.debug("jobId {} found !".format(job_id))
            return jsonify(db_result), 200

        else:
            response = "jobId {} not found".format(job_id)
            app.logger.debug(response)
            return jsonify({'message': "Not found", "jobId": job_id}), 400
    except(Exception) as error:
        app.logger.error(error)
        return '', 503


############################################################################
# Main function
############################################################################
if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Hello world application")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 80))

    if ARGS.debug:
        app.logger.debug("Running in debug mode")
        app.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        app.run(host='0.0.0.0', port=PORT, debug=False)
