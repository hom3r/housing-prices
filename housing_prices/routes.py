#!/usr/bin/env python3
# encoding: utf-8

from sys import stderr
from http import HTTPStatus
from flask import Blueprint, request, jsonify, render_template
from jsonschema import validate, exceptions
from flasgger import swag_from
from lorem import get_paragraph
import werkzeug.exceptions as server_exceptions

from .config import config, house_schema, houses_schema, features
from .predictor import Predictor

pages = Blueprint('basic_pages', __name__)
api = Blueprint('api', __name__)

api_prefix = config['api_prefix']
docs_url = config['docs_url']
batch_limit =config['batch_limit']

predictor = Predictor(config['model_path'], features)


@api.route('/predict-price', methods=['POST'])
@swag_from('swagger/predict-price.yml')
def predict_price():
    """
    Predicts house price based on its parameters.
    """
    try:
        # get the house parameters and validate them
        house = request.json
        validate(instance=house, schema=house_schema)

        price = predictor.predict_price(house)

        return jsonify({'predicted_house_price': price})
    except server_exceptions.BadRequest as ex:
        # bad request due to invalid JSON format
        return error('Bad request. The JSON in request body is invalid.'), HTTPStatus.BAD_REQUEST
    except exceptions.ValidationError as ex:
        # bad request due to JSON validation reason
        return error(ex.message), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        # unknown error
        print(ex, file=stderr)
        return error('Internal server error.'), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route('/predict-prices', methods=['POST'])
@swag_from('swagger/predict-prices.yml')
def predict_prices():
    """
    Predicts prices of multiple houses based on their parameters.
    """
    try:
        # get the house parameters
        houses = request.json

        if len(houses) > batch_limit:
            return error(F'The array of houses is too big. Max size of the batch is {batch_limit} items per request.'), HTTPStatus.BAD_REQUEST
        
        # validate the data
        validate(instance=houses, schema=houses_schema)

        if houses == []:
            # empty input array produces empty output array
            prices = []
        else:
            prices = predictor.predict_prices(houses)

        return jsonify({'predicted_house_prices': prices})

    except server_exceptions.BadRequest as ex:
        # bad request due to invalid JSON format
        return error('Bad request. The JSON in request body is invalid.'), HTTPStatus.BAD_REQUEST
    except exceptions.ValidationError as ex:
        # bad request due to JSON validation reason
        return error(ex.message), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        # unknown error
        print(ex, file=stderr)
        return error('Internal server error.'), HTTPStatus.INTERNAL_SERVER_ERROR


###############################################
# some support routes below

@pages.route('/tos')
def tos():
    """
    Describes the terms of service.
    """
    lipsum = ''.join([F'<p>{get_paragraph()}</p>' for _ in range(42)])
    content = F"""
    <h1>Terms of Service</h1>
    <p>These are the terms of using the housing prices API. Do not use for commercial nor illegal purposes.</p>
    {lipsum}
    <p>Congratulations \U0001F389 You finished reading all of the Terms of Service, yay!</p>
    """
    return render_template('index.html', content=content)


@pages.route('/')
def home():
    """
    Root API route.
    """
    content = F"""
    <h1>Housing Prices API</h1>
    <p>Welcome to the Housing prices API. Please continue to the endpoint <a href="{api_prefix}/predict-price">{api_prefix}/predict-price</a> for price prediction.</p>
    <p>You can also see the <a href="{docs_url}">documentation</a>.
    <p>If you feel bored, you can always read the <a href="/tos">Terms of Service</a>.</p>
    """
    return render_template('index.html', content=content)


@api.route('/predict-price', methods=['GET'])
def predict_price_help():
    """
    The instructions you see in the browser when the endpoint is displayed using GET request.
    """
    content = F"""
    <h1>Method Not Allowed</h1>
    <p>The GET method is not supported. Please use the POST request for this endpoint. See the <a href="{docs_url}">documentation</a> for more information.
    """
    return render_template('index.html', content=content), HTTPStatus.METHOD_NOT_ALLOWED


def error(message):
    """Returns error message as a JSON response."""
    return jsonify({'error': message })
