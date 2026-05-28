PKG := yhwh

.PHONY: develop test check build install uninstall clean

develop:
	pip install -e .

test:
	pytest -q

check: test
	python -m yhwh --he --story אמר
	python -m yhwh --she --story ראה
	python -m yhwh -1 -s --completed HYH

build:
	python -m build

install: build
	pip install dist/*.tar.gz

uninstall:
	pip uninstall $(PKG)

clean:
	rm -rf dist build .pytest_cache src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
