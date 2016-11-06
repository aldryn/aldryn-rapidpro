# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="aldryn-rapidpro",
    version='0.2016.11.6.6.1',
    description='RapidPro as an Aldryn Addon.',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-rapidpro',
    packages=find_packages(),
    install_requires=(
        'aldryn-django',
        'aldryn-celery',
        'rapidpro-server==0.2016.11.6.6'
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
    ]
)
