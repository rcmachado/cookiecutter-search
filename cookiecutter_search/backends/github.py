# coding: utf-8
import json

from tornado import gen
from tornado.concurrent import Future
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
        results = yield self.handle_response(response)
        return results

    @gen.coroutine
    def handle_response(self, response):
        """
        Handle GitHub API response
        """
        if response.code == 200:
            decoded_body = json.loads(response.body.decode('utf-8'))
            result = yield self._transform_successful_response(decoded_body)
        elif response.code == 401:
            result = Future()
            result.set_result({
                'error': "We're over quota. Please come back after a few minutes :)"
            })
        else:
            result = Future()
            result.set_result({
                'error': 'An unknown error ocurred: {}'.format(response.code)
            })
        return result

    @gen.coroutine
    def filter_invalid_repositories(self, repository_list):
        """
        Remove repositories that aren't cookiecutter template repos
        """
        request_queue = []
        for repository in repository_list:
            url = repository['contents_url'].replace('{+path}',
                                                     'cookiecutter.json')
            request_queue.append(self.client.fetch(url, raise_error=False,
                                                   method='HEAD'))

        completed_requests = yield request_queue

        valid_repositories = []
        for repository, response in zip(repository_list, completed_requests):
            if response.code == 200:
                valid_repositories.append(repository)

        return valid_repositories

    @gen.coroutine
    def _transform_successful_response(self, response):
        results = []
        items = yield self.filter_invalid_repositories(response['items'])
        for item in items:
            results.append({
                'name': item['full_name'],
                'description': item['description'],
                'url': item['html_url'],
                'stars': item['stargazers_count'],
            })
        return {'results': results}
