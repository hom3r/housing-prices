#!/usr/bin/env python3
# encoding: utf-8

from setuptools import find_packages, setup

setup(
    name='housing_prices',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)