import logging
from logging.config import dictConfig


def configure_log():
    class MyFilter(logging.Filter):
        def filter(self, record):
            if record.levelno > 20:
                return False
            else:
                return True

    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s %(name)s %(message)s',
            }
        },
        'filters': {
            'myfilter': {
                '()': MyFilter
            }
        },
        'handlers': {
            'wsgi_std': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
                'formatter': 'default',
                'level': 'INFO',
                'filters': ['myfilter']
            },
            'wsgi_err': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
                'level': 'WARNING'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi_std','wsgi_err']
        },
        'loggers': {
            'k8s_sandbox': {
                'level': 'INFO',
                'handlers': ['wsgi_std','wsgi_err'],
                'propagate': False
            },
            'werkzeug': {
                'level': 'INFO',
                'handlers': ['wsgi_std','wsgi_err'],
                'propagate': False
            }
        },
        'disable_existing_loggers': True
    })
