#!/usr/bin/env python3
# encoding: utf-8

from locale import normalize
import os

from http import HTTPStatus
import pickle
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
from flask import Flask, Blueprint, request, jsonify, render_template
from flasgger import Swagger, swag_from
from jsonschema import validate, exceptions
from werkzeug import exceptions

features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'ocean_proximity']
schema = {
    'type' : 'object',
    'properties' : {
        'longitude' : { 'type' : 'number' },
        'latitude' : { 'type' : 'number'},
        'housing_median_age': { 'type': 'number'},
        'population': { 'type': 'integer'},
        'households': { 'type': 'integer'},
        'total_rooms': { 'type': 'integer'},
        'total_bedrooms': { 'type': 'integer'},
        'median_income': { 'type': 'number'},
        'ocean_proximity': { 
        'type': 'string', 
        'enum': ['NEAR BAY', '<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'ISLAND'] 
        }
    },
    'required': features
}

swagger_config = {
    'title': 'Housing Prices API',
    'description': 'This API predicts the housing prices based on the property parameters.',
    'uiversion': 3,
    'openapi': '3.0.3',
    'version': '1.0.0',
    'persistAuthorization': True,
    'components': {
        'schemas': {
            'House': schema
        }
    }
}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config

    Swagger(app, config=swagger_config, merge=True)

    app.config.from_mapping()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # TODO use relative path to open the file
    infile = open('/Users/dejv/Dev/python/housing-prices/housing-prices/model.pkl','rb')
    model = pickle.load(infile)
    infile.close()

    # error handling
    @app.errorhandler(404)    
    # inbuilt function which takes error as parameter
    def not_found(e):
        content = """
        <h1>Not Found</h1>
        <p>The requested URL was not found on the server. Please see the documentation on <a href=\"/apidocs\">/apidocs</a>.</p>
        """
        return render_template("index.html", content = content), HTTPStatus.NOT_FOUND

    
    bp = Blueprint('housing-prices', __name__)

    @bp.route('/tos')
    def tos():
        """
        Describes the terms of service.
        """
        content = """
        <h1>Terms of Service</h1>

        <p>These are the terms of using the housing prices API. Do not use for commercial purposes.</p>
        """
        return render_template('index.html', content=content)

    @bp.route('/')
    def home():
        """
        Root API route.
        """
        content = """
        <h1>Housing Prices API</h1>
        <p>Welcome to the Housing prices API. Please continue to the endpoint <a href=\"/predict-price\">/predict-price</a> to for price prediction.</p>
        <p>You can also see the documentation on <a href=\"/apidocs\">/apidocs</a>.
        """
        return render_template('index.html', content=content)

    def error(message):
        """Returns error message as a JSON response."""
        return jsonify({'error': message })

    @bp.route('/predict-price', methods=['GET'])
    def predict_price_help():
        """
        The instructions you see in the browser when the endpoint is displayed using GET request.
        """
        content = """
        <h1>Method Not Allowed</h1>
        <p>The GET method is not supported. Please use the POST request for this endpoint. See the <a href=\"/apidocs\">documentation</a> for more information.
        """
        return render_template('index.html', content=content), HTTPStatus.METHOD_NOT_ALLOWED

    @bp.route('/predict-price', methods=['POST'])
    @swag_from('housing.yml')
    def predict_price():
        """
        Predicts house price based on its parameters.
        """
        try:
            # get the house parameters and validate them
            house = request.json
            validate(instance=house, schema=schema)

            # load model and encoder
            regr = model[0]
            encoder = model[1]

            # create DataFrame
            df = pd.DataFrame(house, index=[0])

            # set the columns in the correct order
            df = df.reindex(columns=features)

            # one-hot encode the ocean proximity
            prox = df['ocean_proximity'].values.reshape(-1, 1)
            ocean_proximity_train = encoder.transform(prox).toarray()

            # replace the categorical value with the encoded array
            df = df.drop('ocean_proximity', axis=1)
            X = np.concatenate((df, ocean_proximity_train),axis=1)

            # normalize data
            X = normalize(X)
            Y = regr.predict(X)
            
            price = Y[0]
            return jsonify({'predicted_house_price': price})
        except exceptions.BadRequest as ex:
            # bad request due to invalid JSON format
            return error('Bad request. The JSON in request body is invalid.'), HTTPStatus.BAD_REQUEST
        except exceptions.ValidationError as ex:
            # bad request due to JSON validation reason
            return error(ex.message), HTTPStatus.BAD_REQUEST
        except Exception as ex:
            # unknown error
            return error('Internal server error.'), HTTPStatus.INTERNAL_SERVER_ERROR

    app.register_blueprint(bp)

    return app