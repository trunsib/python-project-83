PORT ?= 8000

install:
	uv sync --no-install-project

dev:
	uv run flask --debug --app page_analyzer:app run

start-server:
	uv run gunicorn --chdir page_analyzer app:app

setup:
	rm -rf .venv
	uv venv .venv --python 3.10
	uv pip install -r pyproject.toml

build:
	./build.sh
	
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
