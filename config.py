# Configuration variables
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
DEBUG = os.environ.get('DEBUG', False)

MEMCACHE = {
    'SERVERS': os.environ.get('MEMCACHIER_SERVERS', '').split(','),
    'USERNAME': os.environ.get('MEMCACHIER_USERNAME', ''),
    'PASSWORD': os.environ.get('MEMCACHIER_PASSWORD', ''),
    # These came from https://devcenter.heroku.com/articles/memcachier#django
    'OPTIONS': {
        'no_block': True,
        'tcp_nodelay': True,
        'tcp_keepalive': True,
        'remove_failed': 4,
        'retry_timeout': 2,
        'dead_timeout': 10,
        '_poll_timeout': 2000,
    }
}
