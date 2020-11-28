from .settings_common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$7*umdmxez$xypb2^adf&n^7op@v90yd7k7mrng_dp4+4yc&m#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }
#
# postgreSQLへ変更
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog_site',
        'USER': 'postgres',
        'PASSWORD': 'HIRO5152',
#        'USER': os.environ.get('DB_USER'),
#        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ロギングの設定
LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },

        # diaryアプリケーションが利用するロガー
        'diary': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}
