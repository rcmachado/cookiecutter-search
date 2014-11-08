import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, render_template, jsonify
from flask.ext.cache import Cache

import config

app = Flask(__name__)
cache = Cache(app, config=config.CACHE)
req = requests.Session()
req.auth = HTTPBasicAuth(config.GITHUB_TOKEN, 'x-oauth-basic')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search")
def search():
    search_term = request.args.get('q')
    response = _search_for_term(search_term)
    return jsonify(response)


def _search_for_term(search_term):
    response = search_repositories(search_term)
    return _parse_response(response)


@cache.memoize(timeout=3600 * 24)
def search_repositories(search_term):
    url = ('https://api.github.com/search/repositories'
           '?q=cookiecutter+{term}+in:name+in:description+in:readme'
           '&sort=stars&order=desc')

    return req.get(url.format(term=search_term))


@cache.memoize(timeout=3600 * 24)
def is_valid_cookiecutter(contents_url):
    """
    Verify if the repository is a valid cookiecutter template

    We check for the presence of cookiecutter.json on the root of repository.
    """
    url = contents_url.replace('{+path}', 'cookiecutter.json')
    response = req.head(url)
    return response.status_code == 200


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
        if is_valid_cookiecutter(item['contents_url']):
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
