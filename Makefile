python := python3.10

LINTING_DIRS := colortool.py tests


.PHONY: check-lint
check-lint:
	$(python) -m isort --check-only --force-single-line-imports $(LINTING_DIRS)
	$(python) -m autoflake --recursive $(LINTING_DIRS)
	$(python) -m autopep8 --diff --recursive --aggressive --ignore=E501,W503,E701,E704,E721,E741,I100,I201,W504 --exclude=musictool/util/wavfile.py $(LINTING_DIRS)
	$(python) -m unify --recursive $(LINTING_DIRS)
	# $(python) -m flake8 $(LINTING_DIRS)

.PHONY: fix-lint
fix-lint:
	$(python) -m isort --force-single-line-imports $(LINTING_DIRS)
	$(python) -m autoflake --recursive --in-place $(LINTING_DIRS)
	$(python) -m autopep8 --in-place --recursive --aggressive --ignore=E501,W503,E701,E704,E721,E741,I100,I201,W504 --exclude=musictool/util/wavfile.py $(LINTING_DIRS)
	$(python) -m unify --recursive --in-place $(LINTING_DIRS)

.PHONY: check-mypy
mypy:
	$(python) -m mypy $(LINTING_DIRS)

.PHONY: test
test:
	$(python) -m pytest tests

.PHONY: check
check: check-lint mypy test
