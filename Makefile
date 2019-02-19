VIRTUAL_ENV := .env
PRE_DEPS := .env

.env:
	virtualenv --python=python3 .env
	$(VIRTUAL_ENV)/bin/pip install -U pip setuptools

clean:
	find . -name '*.pyc' -delete
	find . -type d -name __pycache__ -exec rm -r {} \+
	git clean -fd

deps: $(PRE_DEPS)
	$(VIRTUAL_ENV)/bin/pip install -e .

test: deps
	$(VIRTUAL_ENV)/bin/pytest

startnotebook: deps
	$(VIRTUAL_ENV)/bin/jupyter notebook notebooks

# builds wheel and dependencies in wheels directory
build: deps
	$(VIRTUAL_ENV)/bin/python setup.py bdist_wheel -d wheels;

lint:
	for file in $$(find . -name "*.py" ! -path */$$VIRTUAL_ENV/*); do pycodestyle $$file; done

.PHONY: build clean lint test deps