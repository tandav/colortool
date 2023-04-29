.PHONY: test
test:
	pytest

.PHONY: bumpver
bumpver:
	# usage: make bumpver PART=minor
	bumpver update --no-fetch --$(PART)

.PHONY: doctest
doctest:
	python -m doctest README.md
