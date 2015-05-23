# coding: utf-8
import os

from tornado.web import StaticFileHandler, url

from cookiecutter_search import handlers


urlpatterns = (
    url(r'/', handlers.IndexHandler, name='index'),
    url(r'/search', handlers.SearchHandler, name='search'),
    url(r'/(googleab9b146cb86fad01\.html)', StaticFileHandler,
        {'path': os.path.join(os.path.dirname(__file__), 'public')})
)
