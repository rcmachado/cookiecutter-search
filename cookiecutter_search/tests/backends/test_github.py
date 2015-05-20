# coding: utf-8
import pytest
from tornado.testing import AsyncTestCase, gen_test

from cookiecutter_search.backends.github import (APIBadCredentialsError,
                                                 APIOverQuotaError, APIError,
                                                 GitHub)
from cookiecutter_search.tests import fixtures


class GitHubTest(AsyncTestCase):
    def setUp(self):
        super(GitHubTest, self).setUp()
        self.github = GitHub('token')

    @gen_test
    def test_search_should_call_api_with_term(self):
        self.github.client.fetch = fixtures.setup_fetch_mock(200, b"")
        yield self.github.search('something')

        url_arg = self.github.client.fetch.call_args[0][0]
        assert self.github.client.fetch.called is True
        assert 'q=cookiecutter+something' in url_arg

    @gen_test
    def test_search_must_return_parsed_response(self):
        self.github.client.fetch = fixtures.github_api_search_successful()

        expected_response = [
            {
                "name": "audreyr/cookiecutter",
                "description": ("A command-line utility that creates projects "
                                "from cookiecutters (project templates). E.g. "
                                "Python package projects, jQuery plugin "
                                "projects."),
                "url": "https://github.com/audreyr/cookiecutter",
                "stars": 1265,
            },
            {
                "name": "audreyr/cookiecutter-pypackage",
                "description": ("Cookiecutter template for a Python package. "
                                "See https://github.com/audreyr/cookiecutter."),  # pragma: noqa
                "url": "https://github.com/audreyr/cookiecutter-pypackage",
                "stars": 315,
            },
            {
                "name": "mapbox/pyskel",
                "description": "Skeleton of a Python package",
                "url": "https://github.com/mapbox/pyskel",
                "stars": 149,
            },
            {
                "name": "pydanny/cookiecutter-djangopackage",
                "description": ("A cookiecutter template for creating "
                                "reusable Django packages quickly. "),
                "url": "https://github.com/pydanny/cookiecutter-djangopackage",
                "stars": 64,
            },
            {
                "name": "lgiordani/postage",
                "description": "A RabbitMQ-based component Python library",
                "url": "https://github.com/lgiordani/postage",
                "stars": 21,
            },
        ]

        response = yield self.github.search('something')
        assert expected_response == response

    @gen_test
    def test_api_rate_limit_exceeded(self):
        self.github.client.fetch = fixtures.github_api_rate_limit_exceeded()

        with pytest.raises(APIOverQuotaError):
            yield self.github.search('something')

    @gen_test
    def test_bad_credentials_supplied(self):
        self.github.client.fetch = fixtures.github_api_bad_credentials()

        with pytest.raises(APIBadCredentialsError):
            yield self.github.search('something')

    @gen_test
    def test_unknown_error_returned(self):
        self.github.client.fetch = fixtures.github_api_unknown_error()

        with pytest.raises(APIError):
            yield self.github.search('something')

    @gen_test
    def test_should_filter_out_invalid_results(self):
        self.github.client.fetch = fixtures.github_api_search_successful()

        yield self.github.search('something')

        # github.client.fetch.call_args_list
        assert self.github.client.fetch.call_count == 6
