# coding: utf-8
from tornado.ioloop import IOLoop

from cookiecutter_search import config
from cookiecutter_search.application import MainApplication
from cookiecutter_search.urls import urlpatterns


if __name__ == '__main__':
    app_config = {
        'debug': config.DEBUG,
        'static_path': 'cookiecutter_search/static/',
        'template_path': 'cookiecutter_search/templates/'
    }
    app = MainApplication(urlpatterns, **app_config)
    app.listen(config.PORT)
    IOLoop.instance().start()
