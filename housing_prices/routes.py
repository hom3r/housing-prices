#!/usr/bin/env python3
# encoding: utf-8

from http import HTTPStatus
from flask import Blueprint, request, jsonify, render_template
from jsonschema import validate, exceptions
from flasgger import swag_from
import werkzeug.exceptions as server_exceptions

from .config import features, house_schema, houses_schema, model_path
from .predictor import Predictor

pages = Blueprint('basic_pages', __name__)
predictor = Predictor(model_path, features)


@pages.route('/predict-price', methods=['POST'])
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
        return error('Internal server error.'), HTTPStatus.INTERNAL_SERVER_ERROR


@pages.route('/predict-prices', methods=['POST'])
@swag_from('swagger/predict-prices.yml')
def predict_prices():
    """
    Predicts prices of multiple houses based on their parameters.
    """
    try:
        # get the house parameters and validate them
        houses = request.json
        validate(instance=houses, schema=houses_schema)

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
        return error('Internal server error.'), HTTPStatus.INTERNAL_SERVER_ERROR


###############################################
# some support routes below

@pages.route('/tos')
def tos():
    """
    Describes the terms of service.
    """
    content = """
    <h1>Terms of Service</h1>

    <p>These are the terms of using the housing prices API. Do not use for commercial purposes.</p>
    """
    return render_template('index.html', content=content)


@pages.route('/')
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


@pages.route('/predict-price', methods=['GET'])
def predict_price_help():
    """
    The instructions you see in the browser when the endpoint is displayed using GET request.
    """
    content = """
    <h1>Method Not Allowed</h1>
    <p>The GET method is not supported. Please use the POST request for this endpoint. See the <a href=\"/apidocs\">documentation</a> for more information.
    """
    return render_template('index.html', content=content), HTTPStatus.METHOD_NOT_ALLOWED


def error(message):
    """Returns error message as a JSON response."""
    return jsonify({'error': message })
