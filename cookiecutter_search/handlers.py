# coding: utf-8

from tornado import gen
from tornado.web import RequestHandler, HTTPError

from cookiecutter_search import config
from cookiecutter_search.backends import GitHub
from cookiecutter_search.cache import Memcache


class BaseHandler(RequestHandler):
    pass


class IndexHandler(BaseHandler):
    def get(self):
        return self.render('index.html')


class SearchHandler(BaseHandler):
    def prepare(self):
        token = getattr(config, 'GITHUB_TOKEN')
        if not token:
            raise HTTPError(500, 'Server misconfigured')

        self.github = GitHub(token)
        self.cache = Memcache()

    @gen.coroutine
    def get(self):
        term = self.get_query_argument('q', None)
        cache_key = 'term={}'.format(term)
        response = self.cache.get(cache_key)

        if response is None:
            response = yield self.github.search(term)
            self.cache.set(cache_key, response, 3600 * 24)

        self.write({'results': response})
