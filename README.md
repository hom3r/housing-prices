# Housing prices prediction API

## Setup

Preferably create the Python evironment first. You need to do this initial step only once.
```
python3 -m venv venv
```

Then activate the environment
```
. venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

Install the application package
```
pip install -e .
```

Unzip the pickled model file
```
tar -zxvf housing_prices/model.tgz
```


## Usage
Set up the env variables
```
export FLASK_ENV=development
export FLASK_APP=housing-prices
```

Run the application
```
flask run
```

The API endpoint is now available at the http://localhost:5000/price-prediction URL.

There is also Swagger documentation for the whole API on http://localhost:5000/apidocs/.

## Docker
To run app in Docker, use the docker-compose tool.
```
docker-compose up
```