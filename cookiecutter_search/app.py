import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, render_template, jsonify
from flask.ext.cache import Cache

import config

app = Flask(__name__)
cache = Cache(app, config=config.CACHE)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search")
def search():
    search_term = request.args.get('q')
    response = _search_for_term(search_term)
    return jsonify(response)


def _search_for_term(search_term):
    response = _make_request(search_term)
    return _parse_response(response)


@cache.memoize(timeout=300)
def _make_request(search_term):
    basic_auth = HTTPBasicAuth(config.GITHUB_TOKEN, 'x-oauth-basic')
    url = ('https://api.github.com/search/repositories?q="cookiecutter%20'
           'template"+{term}+in:name+in:description&sort=stars&order=desc')

    return requests.get(url.format(term=search_term), auth=basic_auth)


def _parse_response(response):
    if response.status_code == 401:
        response = {
            'error': "We're over quota. Please come back after a few minutes :)"
        }
    elif response.status_code == 200:
        response = _transform_response(response)
    else:
        response = {
            'error': 'An unknown error ocurred: {}'.format(response.status_code)
        }

    return response


def _transform_response(github_response):
    response = []
    items = github_response.json().get('items', [])
    for item in items:
        response.append({
            'name': item['full_name'],
            'description': item['description'],
            'url': item['html_url'],
            'stars': item['stargazers_count'],
        })
    return {'results': response}


if __name__ == "__main__":
    app.debug = config.DEBUG
    app.run()
