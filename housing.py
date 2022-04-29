#!/usr/bin/env python3
# encoding: utf-8

from http import HTTPStatus
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from jsonschema import validate
import jsonschema

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
        'ocean_proximity': { 'type': 'string', 'enum': ['NEAR BAY', '<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'ISLAND'] }
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

@app.route('/predict-price', methods=['POST'])
@swag_from('housing.yml')
def hello():
    """
    Predicts house price based on its parameters.
    """
    house = request.json
    print(house)

    try:
      validate(instance=house, schema=schema)
    except jsonschema.exceptions.ValidationError as ex:
      print(ex)
      return jsonify({'error': ex.message }), HTTPStatus.BAD_REQUEST

    # TODO calculate the predicted price instead of squared longitude
    price = house['longitude'] ** 2

    round_price = round(price, 2)
    return jsonify({'predicted_house_price': round_price})

if __name__ == '__main__':
    app.run(debug=True)