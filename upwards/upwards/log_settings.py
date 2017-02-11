LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'upwards/logs/apps.log',
            'when': 'M',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        ''''':{
            'handlers': ['file'],
            'propagate': True,
            'level': 'ERROR',
        },'''
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'ERROR',
        },

        'social': {
            'handlers': ['file'],
            'level': 'ERROR',
        },

    },
}
