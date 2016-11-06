# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="aldryn-rapidpro",
    version='0.0.0.1',
    description='RapidPro as an Aldryn Addon.',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-rapidpro',
    packages=find_packages(),
    install_requires=(
        'aldryn-django',
        'aldryn-celery',

        'django-extensions',
        'django-guardian',
        'pisa',   # ==3.0.33
        'celery[redis]',  # aldryn-celery does not install the redis deps. ==3.1.23
        'python-gcm',
        'pytz',

        'django-compressor<2',  # TODO: try newer version
        'hamlpy',

        'django_select2',
        'django-redis<4',
        'redis',  # was ==2.10.1
        'BeautifulSoup',
        'xlutils',
        'phonenumbers',
        'django-countries<4',  # TODO: try newer version

        'djangorestframework<3.5',  # 3.5.x fails due to missing serializers.MANY_RELATION_KWARGS
        'djangorestframework-xml',
        'iptools',
        'requests',
        'unidecode',

        'stripe',

        'django-timezones',
        'colorama',
        'isoweek==1.2.0',  # TODO: restriction needed?
        'iso639==0.1.1',  # TODO: restriction needed?
        'twilio',
        'pycrypto',
        'numpy',
        'analytics-python',
        'google',
        'ply',
        'uservoice',
        'geojson==1.0.7',  # TODO: restriction needed?
        'pycountry==1.18',  # TODO: restriction needed?
        'stop-words',
        'twython',
        'enum34',
        'plivo',
        'rapidpro-expressions',
        'python-telegram-bot',
        'django-mptt==0.7.4',  # TODO: restriction needed?
        'openpyxl',
        'django-excel',
        'pyexcel-xls',
        'pyexcel-xlsx',

        'smartmin',
        'librato_bg',

        # 'https://github.com/nyaruka/django-modeltranslation/archive/dffebc9363297d77d91c99d46e8e53b32dc05e61.zip#egg=django_modeltranslation',

        # only adding my quickblocks fork here because of the ancient Pillow requirement it depends on.
        # (That Pillow version does not compile)
        # 'https://github.com/stefanfoulis/django-quickblocks/archive/fix/pillow-dependency.zip#egg=django-quickblocks==0.9.2',

        # 'https://github.com/caktus/django-ttag/archive/40c97c01325d436f5d04529526fa7468ff778137.zip#egg=django-ttag',

        # 'https://github.com/nyaruka/django-celery-transactions/archive/f7adf7f2d5ce0bcd7992e0d4f3624fb96a7d80b8.zip#egg=django-celery-transactions',

        # because of LIKE, ILIKE and IEXACT support, which is not in upstream. Does not need to be this specific commit (can be master).
        # 'https://github.com/nyaruka/django-hstore/archive/86b461464db2ad99f62c3ea15afad4022f5c0df4.zip#egg=django-hstore',

    ),
    entry_points='''
        [console_scripts]
        aldryn-celery=aldryn_celery.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
    ]
)
