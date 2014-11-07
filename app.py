import pylibmc
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, render_template, jsonify

import config

app = Flask(__name__)
cache = pylibmc.Client(config.MEMCACHE['SERVERS'], binary=True,
                       behaviors=config.MEMCACHE['OPTIONS'])

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search")
def search():
    search_term = request.args.get('q')
    response = _search_for_term(search_term)
    return jsonify(response)


def _search_for_term(search_term):
    cache_key = 's-{}'.format(search_term)
    response = cache.get(cache_key)
    if not response:
        response = _make_request(search_term)
        cache.set(cache_key, response, 3600)
    return response


def _make_request(search_term):
    basic_auth = HTTPBasicAuth(config.GITHUB_TOKEN, 'x-oauth-basic')
    url = ('https://api.github.com/search/repositories?q="cookiecutter%20'
           'template"+{term}+in:description&sort=stars&order=desc')

    github_response = requests.get(url.format(term=search_term),
                                   auth=basic_auth)

    if github_response.status_code == 401:
        response = {
            'error': "We're over quota. Please come back after a few minutes :)"
        }
    elif github_response.status_code == 200:
        response = _transform_response(github_response)
    else:
        response = {
            'error': 'An unknown error ocurred: {}'.format(github_response.status_code)
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
        })
    return {'results': response}


if __name__ == "__main__":
    app.debug = True #config.DEBUG
    app.run()
