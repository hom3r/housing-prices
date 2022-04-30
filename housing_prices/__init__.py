#!/usr/bin/env python3
# encoding: utf-8

import os

from http import HTTPStatus
from flask import Flask, render_template
from flasgger import Swagger

from .config import swagger, api_prefix, docs_url
from .routes import pages, api

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Swagger(app, config=swagger, merge=True)

    app.config.from_mapping()
    app.register_blueprint(pages)
    app.register_blueprint(api, url_prefix=api_prefix)

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


    # error handling
    @app.errorhandler(404)
    def not_found(e):
        content = F"""
        <h1>Not Found</h1>
        <p>The requested URL was not found on the server. Please see the <a href="{docs_url}">documentation</a>.</p>
        """
        return render_template("index.html", content = content), HTTPStatus.NOT_FOUND


    return app
