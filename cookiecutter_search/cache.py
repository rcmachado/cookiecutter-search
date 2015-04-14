# coding: utf-8
import functools
import hashlib

import pylibmc

from cookiecutter_search import config


cfg = dict(config.MEMCACHE)


class Memcache(pylibmc.Client):
    """
    A very basic wrapper around pylibmc.Client

    Just grabs configuration data from config.py and
    initialize cache client with them.
    """
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'binary': True,
            'behaviors': cfg['OPTIONS'],
        });

        if cfg.get('USERNAME'):
            kwargs['username'] = cfg['USERNAME']
        if cfg.get('PASSWORD'):
            kwargs['password'] = cfg['PASSWORD']
        super(Memcache, self).__init__(cfg['SERVERS'], **kwargs)
