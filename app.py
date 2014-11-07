import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, render_template, jsonify

import config

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search")
def search():
    search_term = request.args.get('q')

    basic_auth = HTTPBasicAuth(config.GITHUB_TOKEN, 'x-oauth-basic')
    url = ('https://api.github.com/search/repositories?q="cookiecutter%20'
           'template"+{term}+in:description&sort=stars&order=desc')

    github_response = requests.get(url.format(term=search_term),
                                   auth=basic_auth)

    response = []
    items = github_response.json().get('items', [])
    for item in items:
        response.append({
            'name': item['full_name'],
            'description': item['description'],
            'url': item['html_url'],
        })
    return jsonify({'results': response})


if __name__ == "__main__":
    app.debug = True
    app.run()
