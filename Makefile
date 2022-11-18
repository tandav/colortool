LINTING_DIRS := colortool.py tests


.PHONY: check-lint
check-lint:
	python -m isort --check-only $(LINTING_DIRS)
	python -m autoflake --recursive $(LINTING_DIRS)
	python -m autopep8 --diff $(LINTING_DIRS)
	python -m flake8 $(LINTING_DIRS)

.PHONY: fix-lint
fix-lint:
	python -m isort $(LINTING_DIRS)
	python -m autoflake --recursive --in-place $(LINTING_DIRS)
	python -m autopep8 --in-place $(LINTING_DIRS)

.PHONY: check-mypy
mypy:
	python -m mypy $(LINTING_DIRS)

.PHONY: test
test:
	python -m pytest tests

.PHONY: check
check: check-lint mypy test

.PHONY: bumpver
bumpver:
	# usage: make bumpver PART=minor
	bumpver update --no-fetch --$(PART)
