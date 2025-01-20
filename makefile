#!/usr/bin/make

builddeps:
	pip install -U wheel build twine

wheel:
	python3 -m build

pypi:
	python3 -m twine upload dist/*

clean:
	rm -rf dist build system_calls.egg-info/
