## Getting started

Those instructions will make the ETL job up and running on your local machine for development and testing purposes. 
See [Deployment](https://github.com/Oussama-bch/awesome-etl/blob/master/README.md) section for notes on how to deploy the hole project.

### Prerequisites

Before statring you must have :
* Running MongoDB instance
* Running Redis instance
* Running Postgresql instance

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

## Authors

* **Oussama BEN CHARRADA** - *Initial work*