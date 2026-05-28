PKG := yhwh

PYTHON := python
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
TWINE := $(PYTHON) -m twine

.PHONY: \
	build install develop check uninstall clean \
	push-test pull-test push-prod pull-prod

build:
	$(PIP) install build
	$(PYTHON) -m build

install: clean build
	$(PIP) install dist/*.tar.gz

develop:
	$(PIP) install -e .

check:
	$(PYTEST) -v tests/

uninstall:
	$(PIP) uninstall -y $(PKG)

clean:
	rm -rf dist build .pytest_cache src/*.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

push-test:
	$(PIP) install twine
	$(TWINE) upload --repository testpypi dist/*

pull-test:
	$(PIP) install --index-url https://test.pypi.org/simple/ --upgrade $(PKG)

push-prod:
	$(PIP) install twine
	$(TWINE) upload dist/*

pull-prod:
	$(PIP) install --upgrade $(PKG)
