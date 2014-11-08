# Configuration variables
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
DEBUG = os.environ.get('DEBUG', True)

CACHE = {
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', 'simple'),
    'CACHE_MEMCACHED_SERVERS': [os.environ.get('MEMCACHIER_SERVERS', '127.0.0.1')],
    'CACHE_MEMCACHED_USERNAME': os.environ.get('MEMCACHIER_USERNAME', ''),
    'CACHE_MEMCACHED_PASSWORD': os.environ.get('MEMCACHIER_PASSWORD', ''),
}
