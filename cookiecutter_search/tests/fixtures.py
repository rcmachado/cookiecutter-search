# coding: utf-8
import os
from io import BytesIO
from unittest.mock import MagicMock

from tornado.concurrent import Future
from tornado.httpclient import HTTPRequest, HTTPResponse


def github_api_search_successful():
    body = read_file('fixtures/github_api_search_successful.json')
    responses = [
        (200, body),
        (200, b''),
        (200, b''),
        (200, b''),
        (200, b''),
        (200, b''),
        (200, b''),
    ]

    def side_effect(request, **kwargs):
        if request is not HTTPRequest:
            request = HTTPRequest(request)
        status_code, body = responses.pop(0)
        return create_response(request, status_code, body)

    return MagicMock(side_effect=side_effect)


def github_api_bad_credentials():
    body = (b'{"message": "Bad credentials",'
            b'"documentation_url": "https://developer.github.com/v3"}')
    return setup_fetch_mock(401, body)


def github_api_rate_limit_exceeded():
    body = (b'{"message": "API rate limit exceeded for xxx.xxx.xxx.xxx.",'
            b'"documentation_url": "https://developer.github.com/v3"}')
    return setup_fetch_mock(403, body)


def github_api_unknown_error():
    return setup_fetch_mock(500, b'any error response')


def read_file(filename):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
    return open(path, mode='br').read()


def create_response(request, status_code, body):
    response = HTTPResponse(request, status_code, None, BytesIO(body))
    future = Future()
    future.set_result(response)
    return future


def setup_fetch_mock(status_code, body=None):
    def side_effect(request, **kwargs):
        if request is not HTTPRequest:
            request = HTTPRequest(request)
        return create_response(request, status_code, body)
    return MagicMock(side_effect=side_effect)
