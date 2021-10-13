## Getting started

Those instructions will make the REST API up and running on your local machine for development and testing purposes. 
See [Deployment](https://github.com/Oussama-bch/awesome-etl/blob/master/README.md) section for notes on how to deploy the hole project.

### Prerequisites
Before statring you must have :
* Running MongoDB instance
* Running Redis instance

##### 1- Fill database config file
You must fill [database.ini](https://github.com/Oussama-bch/awesome-etl/blob/master/api/database.ini) with resources created above.
```
[mongodb]
uri=mongodb://[YOUR MACHINE IPv4]:2717
database=etl
collection=jobs

[redis]
host=[YOUR MACHINE IPv4]
port=6379
db=0
channel=etl_jobs
```

## Unit tests
Unit tests must be exectued inside a virtualenv.
##### 1- Activate virtualenv
```
python3 -m venv api_env
source api_env/bin/activate
```

##### 2- Install all requirements
```
pip3 install -r requirements.txt
```
##### 3- Run unit tests
```
python3 -m unittest unit_tests.py -v
```

## Service tests
Service tests must be executed inside a docker container
##### 1- Build docker image
```
docker build -t api:v0.1 .
```

##### 2- Run docker container
```
docker run -d -p 80:80 -v awesome-etl/etl-job-volume:awesome-etl/etl-volume -t api:v0.1
```
##### 3- Tests endpoints
```
# Test POST request:
curl -X POST -H "Content-Type: application/json" \
    -d '{"fileLocation":"awesome-etl/volumes/etl-volume/global_power_plant_database.csv"}' \ 
    http://localhost:80/jobs/start

# Test GET request :
curl -X 'GET' \
  'http://localhost:80/jobs/[jobID]' \
  -H 'accept: application/json'
```

## Authors

* **Oussama BEN CHARRADA** - *Initial work*