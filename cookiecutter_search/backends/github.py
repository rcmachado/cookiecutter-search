# coding: utf-8
import json

from tornado import gen
from tornado.httpclient import AsyncHTTPClient


class APIError(Exception):
    pass


class APIOverQuotaError(APIError):
    pass


class APIBadCredentialsError(APIError):
    pass


class GitHub(object):
    def __init__(self, token):
        conn_options = {
            'auth_username': token,
            'auth_password': 'x-oauth-basic',
            'user_agent': ('CookieCutter Search '
                           '<http://cookiecutter-search.herokuapp.com>'),
        }
        self.client = AsyncHTTPClient(defaults=conn_options)

    @gen.coroutine
    def search(self, term):
        url = ('https://api.github.com/search/repositories'
               '?q=cookiecutter+{term}+in:name+in:description+in:readme'
               '&sort=stars&order=desc').format(term=term)
        response = yield self.client.fetch(url)

        if response.code != 200:
            raise self.handle_error(response.code)

        decoded_body = self.extract_data_from_response(response)
        results = yield self.filter_results(decoded_body)
        return results

    def handle_error(self, status_code):
        if status_code == 403:
            return APIOverQuotaError(
                'API rate limit exceeded. Please check if your auth token is '
                'still valid and the cache is functioning properly.')
        elif status_code == 401:
            return APIBadCredentialsError(
                'Bad credentials informed. Please check if auth token is '
                'still valid and generate another one if needed.')

        return APIError('Unknown error ocurred')

    def extract_data_from_response(self, response):
        content = response.body.decode('utf-8')
        if not content:
            return {}
        return json.loads(content)

    @gen.coroutine
    def filter_results(self, response):
        if not response.get('items'):
            return []

        items = yield self.extract_valid_repositories(response['items'])
        results = []
        for item in items:
            results.append({
                'name': item['full_name'],
                'description': item['description'],
                'url': item['html_url'],
                'stars': item['stargazers_count'],
            })
        return results

    @gen.coroutine
    def extract_valid_repositories(self, repository_list):
        """
        Remove repositories that aren't cookiecutter template repos
        """
        completed_requests = yield self._build_repositories_queue(
            repository_list)

        valid_repositories = []
        for repository, response in zip(repository_list, completed_requests):
            if response.code == 200:
                valid_repositories.append(repository)

        return valid_repositories

    def _build_repositories_queue(self, repository_list):
        requests_queue = []
        for repository in repository_list:
            url = repository['contents_url'].replace('{+path}',
                                                     'cookiecutter.json')
            requests_queue.append(self.client.fetch(url, raise_error=False,
                                                    method='HEAD'))
        return requests_queue
