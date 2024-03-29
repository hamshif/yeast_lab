"""
Django settings for lab project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
import traceback


ADMIN_GROUP_NAME = 'yeast_im'



BASE_DIR = os.path.dirname(os.path.dirname(__file__))

print('settings.Base_DIR: ', BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'v=kf2apx^p_7b5x12cym9*ai9nog0=rfjkkmliap(73$s=vm&k'


DEBUG = True
  
TEMPLATE_DEBUG = True

PRODUCTION_ENVIRONMENT = False
DB_NAME = 'yeast'
PLATE_IMAGE_ROOT = "/cs/wetlab/dev1_yeast_library_images"
LIQUID_PLATE_ROOT = "/cs/wetlab/dev_growth_data"
ANALYZE = False

print('')

if sys.argv:
    
    try:
    
        for arg in sys.argv:
            
            print('sys argument :', arg)

            
        if os.getenv('production', 'false') == 'true':

            print("setting variables for production")

            PRODUCTION_ENVIRONMENT = True
            DB_NAME = 'yeast_prod'
            PLATE_IMAGE_ROOT = "/cs/wetlab/prod_yeast_library_img"


            
        if 'uwsgi' in sys.argv:
         
            print("setting variables for uwsgi")
     
            # DEBUG = False
             
            # TEMPLATE_DEBUG = False

            WSGI_APPLICATION = 'lab.wsgi.application'
            
            # print('using temp DB and image directory for debugging production environment')

            LOGGING = {
            'version': 1,
            'formatters': {
                'verbose': {
                    'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                },
                'simple': {
                    'format': '%(levelname)s %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                    },
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': '/var/log/wetlab/django_uwsgi.log',
                    'formatter': 'simple'
                    },
                },
            'loggers': {
                'django': {
                    'handlers': ['file'],
                    'level': 'DEBUG',
                    'propagate': True,
                    },
                }
            }




        else:
            print("remained with default variables set for development environment")


        if os.getenv('analyze', 'false') == 'true':

            ANALYZE = True


            
    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()


print('')
print('PRODOCTION_ENVIRONMENT: ', PRODUCTION_ENVIRONMENT)
print('DB_NAME: ', DB_NAME)
print('PLATE_IMAGE_ROOT: ', PLATE_IMAGE_ROOT)
print('ANALYZE: ', ANALYZE)
    

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.load_template_source',
#     'django.template.loaders.app_directories.load_template_source',

# #    'django.template.loaders.eggs.load_template_source',

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ALLOWED_HOSTS = ['e-cab-27.cs.huji.ac.il', 
                 'pe-01m.cs.huji.ac.il',
                 'e-cab-27',
                 'pe-01m',
                 'wetlab',
                 'wetlab.cs.huji.ac.il',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lab',
    'yeast_libraries',
    'mediums',
    'suppliers',
    'cmd_utils',
    'image_analysis',
    'excels',
    'yeast_liquid_plates',
)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lab.urls'




# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,            # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'cab-27',                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)




MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
print('STATIC_ROOT: ', STATIC_ROOT)

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/ 


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nu*@78!uk9o5(nyiqfgj1*kn9cka0fwuz@d8@w#bjz^%jm-vgm'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
# #            'filename': '/cs/system/gideonbar/tmp_wet/django_log/debug.log',
#             'filename': '/tmp/django.log',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
