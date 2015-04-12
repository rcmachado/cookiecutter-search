# coding: utf-8
import json

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPError


class GitHub(object):
    def __init__(self, token):
        conn_options = {
            'auth_username': token,
            'auth_password': 'x-oauth-basic',
            'user_agent': ('CookieCutter Search '
                           '<http://cookiecutter-search.herokuapp.com>'),
        }
        self.client = AsyncHTTPClient(defaults=conn_options)

    def get_url(self, term):
        return ('https://api.github.com/search/repositories'
                '?q=cookiecutter+{term}+in:name+in:description+in:readme'
                '&sort=stars&order=desc').format(term=term)

    # Cache this
    @gen.coroutine
    def search(self, term):
        url = self.get_url(term)
        response = yield self.client.fetch(url)
        if response.code == 200:
            result = self._transform_successful_response(json.loads(response.body.decode('utf-8')))
        else:
            result = self._handle_error(response)
        return result

    # Cache this forever - this (normally) don't change
    @gen.coroutine
    def is_template_repo(self, base_content_url):
        url = base_content_url.replace('{+path}', 'cookiecutter.json')
        try:
            response = yield self.client.fetch(url)
        except HTTPError:
            return False
        return response.code == 200

    def _handle_error(self, response):
        if response.code == 401:
            result = {
                'error': "We're over quota. Please come back after a few minutes :)"
            }
        else:
            result = {
                'error': 'An unknown error ocurred: {}'.format(response.code)
            }
        return result

    # Cache this
    def _transform_successful_response(self, response):
        results = []
        items = response.get('items', [])
        for item in items:
            if self.is_template_repo(item['contents_url']):
                results.append({
                    'name': item['full_name'],
                    'description': item['description'],
                    'url': item['html_url'],
                    'stars': item['stargazers_count'],
                })
        return {'results': results}
