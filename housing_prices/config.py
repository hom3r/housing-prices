features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'ocean_proximity']

house_schema = {
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

houses_schema = {
    'type': 'array',
    'items': house_schema
}

config = {
    'model_path': 'data/model.pkl',
    'api_prefix': '/v1',
    'batch_limit': 1000,
    'docs_url': '/v1/apidocs',

    'swagger': {
        'title': 'Housing Prices API',
        'description': 'This API predicts the housing prices based on the property parameters.',
        'uiversion': 3,
        'openapi': '3.0.3',
        'version': '1.0.0',
        'persistAuthorization': True,
        'url_prefix': '/v1',
        'specs_route': '/apidocs/',
        'components': {
            'schemas': {
                'House': house_schema
            }
        },
        'specs': [
            {
                'endpoint': '/v1',
                'route': '/swagger.json',
            }
        ],
    }
}

