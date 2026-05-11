PORT ?= 8000

install:
	uv sync --no-install-project

dev:
	uv run flask --debug --app page_analyzer:app run

setup:
	rm -rf .venv
	uv venv .venv
	uv pip install -r pyproject.toml

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh
	
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
