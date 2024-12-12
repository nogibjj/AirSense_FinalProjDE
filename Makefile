install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python3 -m pytest -vv --cov=services/connector services/connector/test.py &&\
	python3 -m pytest -vv --cov=services/gateway services/gateway/test.py

format:
	black services/**/*.py

lint:
	ruff check services/**/*.py

refactor: format lint

all: install lint test format
