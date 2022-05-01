# Housing prices prediction API

This API provides a prediction model, which estimates the price of a property given neighborhood such as number of households, population, proximity to the ocean etc..

Please read below to see how to run the application either using Docker (production) or Flask (development). 

In both cases the app will by default run on http://localhost:5000/.

The price prediction API endpoint is available at the http://localhost:5000/v1/predict-price URL. Note that you have to use POST request with the valid JSON payload.

## API Documentation

See the Swagger documentation with executable examples for the whole API on http://localhost:5000/v1/apidocs/.


## Production
You are encouraged to use Docker for building and running the application in a container in the production environment. To run the app, use docker-compose
```
docker-compose up
```

Application should now run on http://localhost:5000/.

To change the port (default is 5000), edit the `docker-compose.yml` file.

```
# ...
    ports:
      - 5000:80     # replace 5000 with your desired port number
# ...
```

The application is deployment ready. It is served using uWSGI and nginx for best production performance. If you need to tweak the production parameters like number of processes (4 by default) etc, edit the `.docker/uwsgi.ini` file (at your own risk). 


## Development

### Setup

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
tar -zxvf data/model.tgz
```


### Usage
Set up the env variables
```
export FLASK_ENV=development
export FLASK_APP=housing_prices
```

Run the application
```
flask run
```

Application should now run on http://localhost:5000/.

