# coding: utf-8

from tornado import gen
from tornado.web import RequestHandler, HTTPError

from cookiecutter_search import config
from cookiecutter_search.backends import GitHub


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

    @gen.coroutine
    def get(self):
        term = self.get_query_argument('q', None)
        response = yield self.github.search(term)
        self.write(response)
