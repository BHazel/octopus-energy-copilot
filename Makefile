BUILD_DIRS=build dist *.egg-info __pycache__

all: build-cli

build-cli:
	cd cli && \
	make

init:
	python -m venv .venv
	cp .env-sample cli/cli/.env

test:
	python -m unittest

clean:
	for dir in $(BUILD_DIRS); do \
		find . -type d -name "$$dir" -exec rm -rf {} +; \
	done

distclean: clean
	rm -rf ./.venv