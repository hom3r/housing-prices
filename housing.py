#!/usr/bin/env python3
# encoding: utf-8

from http import HTTPStatus
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from jsonschema import validate
import jsonschema
from werkzeug import exceptions

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
    'required': ['longitude', 'latitude', 'housing_median_age','population','households','total_rooms','total_bedrooms','median_income','ocean_proximity']
}


app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Housing Prices API',
    'description': 'This API predicts the housing prices based on the property parameters.',
    'uiversion': 3,
    'openapi': '3.0.3',
    'version': '0.1.0',
    'persistAuthorization': True,
    'components': {
      'schemas': {
        'House': schema
      }
    }
}

swagger = Swagger(app)

@app.route('/tos')
def tos():
  """
  Describes the terms of service.
  """
  return """
  <h1>TERMS OF SERVICE</h1>

  <p>These are the terms of using the housing prices API. Do not use for commercial purposes.</p>
  """

@app.route('/')
def home():
  """
  Root API route.
  """
  return """
  <h1>Housing Prices API</h1>
  <p>Welcome to the Housing prices API. Please continue to the endpoint <a href=\"/predict-price\">/predict-price</a> to for price prediction.</p>
  <p>You can also see the documentation on <a href=\"/apidocs\">/apidocs</a>.
  """


@app.route('/predict-price', methods=['GET'])
def predict_price_help():
  """
  The instructions you see in the browser when the endpoint is displayed using GET request.
  """
  return """
  <h1>Method Not Allowed</h1>
  <p>The GET method is not supported. Please use the POST request for this endpoint. See the <a href=\"/apidocs\">documentation</a> for more information.
  """, HTTPStatus.METHOD_NOT_ALLOWED

def error(message):
  """Returns error message as a JSON response."""
  return jsonify({'error': message })


@app.route('/predict-price', methods=['POST'])
@swag_from('housing.yml')
def predict_price():
    """
    Predicts house price based on its parameters.
    """
    try:
      house = request.json
      validate(instance=house, schema=schema)
    except exceptions.BadRequest as ex:
      # bad request due to invalid JSON format
      return error('Bad request. The JSON in request body is invalid.'), HTTPStatus.BAD_REQUEST
    except jsonschema.exceptions.ValidationError as ex:
      # bad request due to JSON validation reason
      return error(ex.message), HTTPStatus.BAD_REQUEST
    except Exception as ex:
      # unknown error
      return error('Internal server error.'), HTTPStatus.INTERNAL_SERVER_ERROR

    # TODO calculate the predicted price instead of squared longitude
    price = house['longitude'] ** 2

    round_price = round(price, 2)
    return jsonify({'predicted_house_price': round_price})

if __name__ == '__main__':
    app.run(debug=True)