.PHONY: setup
GIT_BRANCH=$(shell git branch |grep -e "^\*"|cut -d" " -f2)

setup: venv
	venv/bin/python setup.py develop
	venv/bin/pip install -r requirements.txt

venv:
	virtualenv venv

clean:
	rm -rf dist build noonoo.egg-info

lint:
	flake8 noonoo

release:
	@git checkout v$(VERSION)
	@-rm dist/*
	venv/bin/python setup.py sdist bdist_wheel
	@read -n 1 -r -p "Release $(VERSION) to PyPI? " REPLY; \
	if [ "$$REPLY" == "y" ]; then\
		twine upload dist/*.tar.gz;\
		twine upload dist/*.whl;\
	else\
		echo "Not uploading..";\
	fi
	git checkout $(GIT_BRANCH)

release_test:
	venv/bin/python setup.py sdist bdist_wheel upload -r pypitest

version:
	git tag -a v$(VERSION)
