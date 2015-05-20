.SILENT:

all: install clean test

clean:
	find . -iname '*.pyc' -delete
	rm -rf *.egg-info

install:
	pip install -r requirements.txt

test:
	py.test
