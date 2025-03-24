BUILD_DIRS=build dist *.egg-info

all: build-cli

build-cli:
	cd cli && \
	make

test:
	python -m unittest

clean:
	for dir in $(BUILD_DIRS); do \
		find . -type d -name "$$dir" -exec rm -rf {} +; \
	done