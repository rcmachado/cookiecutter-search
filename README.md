# Cookiecutter search

A search interface for cookiecutter templates.

You could see it running at http://cookiecutter-search.herokuapp.com

## What is cookiecutter?

Cookiecutter is a command-line utility that creates projects from
cookiecutters (project templates). More information can be found at
https://github.com/audreyr/cookiecutter.

## How to install

    $ pip install -r requirements.txt

## Running the app

You need to get a [GitHub OAuth token][oauth_token] and put it on a
`GITHUB_TOKEN` env variable. For example:

    $ GITHUB_TOKEN='your-github-token' python app.py

## License

This project is licensed under MIT license (see LICENSE file for
details). Note that each template has its own licensing terms (and you
must comply with them) as of cookiecutter project.

[oauth_token]: https://developer.github.com/v3/auth/#via-oauth-tokens
