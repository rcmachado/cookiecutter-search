.SILENT:

all: install clean lint test

clean:
	find . -iname '*.pyc' -delete
	rm -rf *.egg-info

install:
	pip install -r requirements.txt

lint:
	flake8 .

test:
	py.test
