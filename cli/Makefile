RELEASE := 0

install: build
	python -m build

build: install-deps
ifeq ($(RELEASE), 1)
	pip install .
else
	pip install --editable .
endif

install-deps:
	pip install build