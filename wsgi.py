#!/usr/bin/env python3
# encoding: utf-8

from housing_prices import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

application = app
