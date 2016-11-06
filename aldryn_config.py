# -*- coding: utf-8 -*-
import os
from aldryn_client import forms


class Form(forms.BaseForm):

    def to_settings(self, data, settings):
        from functools import partial
        from aldryn_addons.utils import boolean_ish, djsenv
        from django.utils.translation import ugettext_lazy as _
        env = partial(djsenv, settings=settings)
        s = settings

        # quickfix so analytics does not explode everywhere
        # TODO: fix rapidpro codebase to work without analytics configured
        s['SEGMENT_IO_KEY'] = env('SEGMENT_IO_KEY', '')
        import analytics
        analytics.write_key = s['SEGMENT_IO_KEY']

        s['LIBRATO_USER'] = env('LIBRATO_USER', '')
        s['LIBRATO_TOKEN'] = env('LIBRATO_TOKEN', '')

        s['TWITTER_API_KEY'] = env('TWITTER_API_KEY', '')
        s['TWITTER_API_SECRET'] = env('TWITTER_API_SECRET', '')

        # The only thing IS_PROD=False seems to do is enable/disable analytics

        s['IS_PROD'] = boolean_ish(env('IS_PROD', False))

        s['STATIC_URL'] = '/static/'

        from temba import settings_common as temba_settings
        s['PERMISSIONS'] = temba_settings.PERMISSIONS
        s['GROUP_PERMISSIONS'] = temba_settings.GROUP_PERMISSIONS
        s['REST_FRAMEWORK'] = temba_settings.REST_FRAMEWORK
        s['AUTHENTICATION_BACKENDS'].extend([
            'smartmin.backends.CaseInsensitiveBackend',
            'guardian.backends.ObjectPermissionBackend',
        ])
        s['ANONYMOUS_USER_NAME'] = 'AnonymousUser'

        import temba
        RAPIDPRO_PACKAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(temba.__file__), '../'))
        s['LOCALE_PATHS'].append(
            os.path.join(RAPIDPRO_PACKAGE_DIR, 'locale')
        )
        RAPIDPRO_STATICFILES_DIR = os.path.join(RAPIDPRO_PACKAGE_DIR, 'static')
        s['STATICFILES_DIRS'].append(RAPIDPRO_STATICFILES_DIR)

        s['LOGIN_URL'] = "/users/login/"
        s['LOGOUT_URL'] = "/users/logout/"
        s['LOGIN_REDIRECT_URL'] = "/org/choose/"
        s['LOGOUT_REDIRECT_URL'] = "/"

        # FIXME: Branding.
        s['DEFAULT_BRAND'] = 'default'
        s['BRANDING'] = {
            'default': {
                'slug': 'rapidpro',
                'name': 'RapidPro',
                'org': 'UNICEF',
                'colors': dict(primary='#0c6596'),
                'styles': ['brands/rapidpro/font/style.css', 'brands/rapidpro/less/style.less'],
                'welcome_topup': 1000,
                'email': 'join@rapidpro.io',
                'support_email': 'support@rapidpro.io',
                'link': 'https://app.rapidpro.io',
                'api_link': 'https://api.rapidpro.io',
                'docs_link': 'http://docs.rapidpro.io',
                'domain': 'app.rapidpro.io',
                'favico': 'brands/rapidpro/rapidpro.ico',
                'splash': '/brands/rapidpro/splash.jpg',
                'logo': '/brands/rapidpro/logo.png',
                'allow_signups': True,
                'tiers': dict(import_flows=0, multi_user=0, multi_org=0),
                'bundles': [],
                'welcome_packs': [dict(size=5000, name="Demo Account"), dict(size=100000, name="UNICEF Account")],
                'description': _("Visually build nationally scalable mobile applications from anywhere in the world."),
                'credits': _("Copyright &copy; 2012-2015 UNICEF, Nyaruka. All Rights Reserved.")
            }
        }
        default_hostname = 'rapidpro.aldryn.me'
        s['HOSTNAME'] = s.get('DOMAIN', default_hostname)
        s['TEMBA_HOST'] = s.get('DOMAIN', default_hostname)

        s['USER_TIME_ZONE'] = 'UTC'
        s['USE_TZ'] = True  # TODO: this should really be in aldryn-django as a default
        s['TIME_ZONE'] = 'UTC'  # TODO: this should really be in aldryn-django as a default
        s['DEFAULT_LANGUAGE'] = s['LANGUAGE_CODE']

        # settings required in migrations, but are probably outdated
        s['AWS_STORAGE_BUCKET_NAME'] = ''
        s['AWS_BUCKET_DOMAIN'] = ''

        s['INSTALLED_APPS'].extend([
            'django.contrib.humanize',
            'django.contrib.sitemaps',
            'redis',
            'guardian',
            'rest_framework',
            'rest_framework.authtoken',
            # compress our CSS and js
            'compressor',

            'smartmin',
            'smartmin.csv_imports',
            'smartmin.users',
            'modeltranslation',

            'timezones',

            'temba.assets',
            'temba.auth_tweaks',
            'temba.api',
            'temba.public',
            'temba.schedules',
            'temba.orgs',
            'temba.contacts',
            'temba.channels',
            'temba.msgs',
            'temba.flows',
            'temba.reports',
            'temba.triggers',
            'temba.utils',
            'temba.campaigns',
            'temba.ivr',
            'temba.locations',
            'temba.values',
            'temba.airtime',
        ])

        s['PERMISSIONS_APP'] = 'temba.airtime'

        # Because of ancient version of django-modeltranslation.
        # Is it REALLY needed?
        s['MODELTRANSLATION_TRANSLATION_REGISTRY'] = 'translation'

        # switch to new style TEMPLATES config?
        loaders = s['TEMPLATES'][0]['OPTIONS']['loaders']
        loaders.insert(0, 'hamlpy.template.loaders.HamlPyFilesystemLoader')
        loaders.insert(1, 'hamlpy.template.loaders.HamlPyAppDirectoriesLoader')

        TEMPLATE_CONTEXT_PROCESSORS = [
            'temba.context_processors.branding',
            'temba.orgs.context_processors.user_group_perms_processor',
            'temba.orgs.context_processors.unread_count_processor',
            'temba.channels.views.channel_status_processor',
            'temba.msgs.views.send_message_auto_complete_processor',
            'temba.api.views.webhook_status_processor',
            'temba.orgs.context_processors.settings_includer',
        ]
        s['TEMPLATES'][0]['OPTIONS']['context_processors'].extend(TEMPLATE_CONTEXT_PROCESSORS)
        if 'EMAIL_CONTEXT_PROCESSORS' not in s:
            s['EMAIL_CONTEXT_PROCESSORS'] = []
        s['EMAIL_CONTEXT_PROCESSORS'].append('temba.utils.email.link_components')

        s['MIDDLEWARE_CLASSES'].insert(
            s['MIDDLEWARE_CLASSES'].index('django.middleware.common.CommonMiddleware'),
            'temba.utils.middleware.DisableMiddleware',
        )
        s['MIDDLEWARE_CLASSES'].extend([
            'temba.middleware.BrandingMiddleware',
            'temba.middleware.OrgTimezoneMiddleware',
            'temba.middleware.FlowSimulationMiddleware',
            'temba.middleware.ActivateLanguageMiddleware',
            'temba.middleware.NonAtomicGetsMiddleware',
        ])

        s['TEMPLATES'][0]['DIRS'].append(
            os.path.join(RAPIDPRO_PACKAGE_DIR, 'templates')
        )

        # There is a lot of unneeded stuff in temba.urls. but for simplicy
        # I'm just including all of them for now.
        s['ADDON_URLS'].append('temba.urls')
        if 'APP_URLS' not in s:
            s['APP_URLS'] = []

        s['SITEMAP'] = [
            'public.public_index',
            'public.public_blog',
            'public.video_list',
            'api',
        ]

        s['LOGGING']['loggers']['pycountry'] = {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        }
        # TODO: put into aldryn-django?
        s['LOGGING']['loggers']['django.db.backends'] = {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        }

        # django-compressor  TODO: cleanup for deployment
        if 'compressor.finders.CompressorFinder' not in s['STATICFILES_FINDERS']:
            s['STATICFILES_FINDERS'].append('compressor.finders.CompressorFinder')
        s['COMPRESS_PRECOMPILERS'] = (
            ('text/less', 'lessc --include-path="%s" {infile} {outfile}' % os.path.join(RAPIDPRO_STATICFILES_DIR, 'less')),
            ('text/coffeescript', 'coffee --compile --stdio'))
        s['COMPRESS_OFFLINE_CONTEXT'] = dict(STATIC_URL=s['STATIC_URL'], base_template='frame.html')

        s['COMPRESS_ENABLED'] = False
        s['COMPRESS_OFFLINE'] = False

        # defaults are STATIC_URL and STATIC_ROOT
        # s['COMPRESS_URL'] = s['STATIC_URL']
        # s['COMPRESS_ROOT'] = s['STATIC_ROOT']


        s['OUTGOING_PROXIES'] = {}

        s['MESSAGE_HANDLERS'] = temba_settings.MESSAGE_HANDLERS

        ######
        # DANGER: only turn this on if you know what you are doing!
        #         could cause messages to be sent to live customer aggregators
        s['SEND_MESSAGES'] = boolean_ish(env('RAPIDPRO_SEND_MESSAGES', False))

        ######
        # DANGER: only turn this on if you know what you are doing!
        #         could cause external APIs to be called in test environment
        s['SEND_WEBHOOKS'] = boolean_ish(env('RAPIDPRO_SEND_WEBHOOKS', False))

        ######
        # DANGER: only turn this on if you know what you are doing!
        #         could cause emails to be sent in test environment
        s['SEND_EMAILS'] = boolean_ish(env('RAPIDPRO_SEND_EMAILS', False))

        ######
        # DANGER: only turn this on if you know what you are doing!
        #         could cause airtime transfers in test environment
        s['SEND_AIRTIME'] = boolean_ish(env('RAPIDPRO_SEND_AIRTIME', False))

        s['IP_ADDRESSES'] = []

        CELERYBEAT_SCHEDULE = s.setdefault('CELERYBEAT_SCHEDULE', {})
        CELERYBEAT_SCHEDULE.update(temba_settings.CELERYBEAT_SCHEDULE)

        # Mapping of task name to task function path, used when CELERY_ALWAYS_EAGER is set to True
        CELERY_TASK_MAP = s.setdefault('CELERY_TASK_MAP', {})
        CELERY_TASK_MAP.update(temba_settings.CELERY_TASK_MAP)

        s['MAGE_API_URL'] = env('MAGE_API_URL', '')
        s['MAGE_AUTH_TOKEN'] = env('MAGE_AUTH_TOKEN', '')
        s['HUB9_ENDPOINT'] = env('HUB9_ENDPOINT', '')
        return settings
