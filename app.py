# coding: utf-8
from tornado.ioloop import IOLoop

from cookiecutter_search.application import MainApplication
from cookiecutter_search.urls import urlpatterns


if __name__ == '__main__':
    config = {
        'static_path': 'cookiecutter_search/static/',
        'template_path': 'cookiecutter_search/templates/'
    }
    app = MainApplication(urlpatterns, **config)
    app.listen(8888)
    IOLoop.instance().start()
