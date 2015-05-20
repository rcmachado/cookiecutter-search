.SILENT:

all: install clean lint test

clean:
	find . -iname '*.pyc' -delete
	rm -rf *.egg-info

install:
	pip install -r requirements.txt

lint:
	flake8 cookiecutter_search app.py

run:
	DEBUG=1 python app.py

test:
	py.test
