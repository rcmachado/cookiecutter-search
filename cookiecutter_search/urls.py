# coding: utf-8
from tornado.web import url

from cookiecutter_search import handlers


urlpatterns = (
    url(r'/', handlers.IndexHandler, name='index'),
    url(r'/search', handlers.SearchHandler, name='search'),
)
