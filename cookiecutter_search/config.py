# coding: utf-8
# Configuration variables
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
DEBUG = os.environ.get('DEBUG', True)
PORT = os.environ.get('PORT', 8888)

MEMCACHE = {
    'SERVERS': os.environ.get('MEMCACHIER_SERVERS', '127.0.0.1').split(','),
    'USERNAME': os.environ.get('MEMCACHIER_USERNAME', ''),
    'PASSWORD': os.environ.get('MEMCACHIER_PASSWORD', ''),
    'OPTIONS': {
        'tcp_nodelay': True,
        'tcp_keepalive': True,
        'ketama': True,
        'no_block': True,
    },
}
