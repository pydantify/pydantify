PROJECT=pydantify
CODE_DIRS=src/${PROJECT} tests

# Run pytest
.PHONY: pytest
pytest:
	uv run pytest -vs ${ARGS}

# Check if the python code needs to be reformatted
.PHONY: black
black:
	uv run black --check ${CODE_DIRS}

# Python type check
.PHONY: mypy
mypy:
	uv run mypy src/${PROJECT}

# Runn pytest, black and mypy
.PHONY: tests
tests: pytest black mypy

# Python type check
.PHONY: diagrams
diagrams:
	uv run pyreverse -o mmd -d docs/resources --project ${PROJECT} --colorized --ignore nodefactory.py,typeresolver.py  src/${PROJECT}/models/
	mv docs/resources/classes_pydantify.mmd docs/resources/classes_models.mmd
	rm docs/resources/packages_pydantify.mmd
	uv run pyreverse -o mmd -d docs/resources --project ${PROJECT} --colorized --filter-mode ALL -S -b src/${PROJECT}/
