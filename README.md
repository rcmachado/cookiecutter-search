# Cookiecutter search

A search interface for cookiecutter templates.

You could see it running at http://cookiecutter-search.herokuapp.com

## What is cookiecutter?

Cookiecutter is a command-line utility that creates projects from
cookiecutters (project templates) created by [Audrey Greenfeld][audrey].
More information can be found at https://github.com/audreyr/cookiecutter.

## How to install

    $ pip install -r requirements.txt

## Running the app

You need to get a [GitHub OAuth token][oauth_token] and put it on a
`GITHUB_TOKEN` env variable. For example:

    $ GITHUB_TOKEN='your-github-token' python app.py

## How it works (for now)

It just search on GitHub for projects that have "cookiecutter templates"
on their description. This allowed a quick PoC in one afternoon but has
some drawbacks - for example, hitting the GitHub API rate limit,
ignoring projects on other VCS services like BitBucket and so on.

The obvious solution is to build an index - but this requires more
thinking into the problem. Probably on another afternoon :)

## Why

This is a proof of concept built at [Python Brasil 10][] after the
keynote by [Daniel Greenfeld][pydanny]. The main reason is, obviously,
find cookiecutter templates more easily. And also because I want to
give back to open source community.

## License

This project is licensed under MIT license (see LICENSE file for
details). Note that each template has its own licensing terms (and you
must comply with them) as of cookiecutter project.

[oauth_token]: https://developer.github.com/v3/auth/#via-oauth-tokens
[Python Brasil 10]: http://2014.pythonbrasil.org.br
[pydanny]: http://pydanny.com
[Audrey]: http://audreyr.com
