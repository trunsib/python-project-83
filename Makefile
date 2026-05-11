PORT ?= 8000

install:
	uv sync --no-install-project

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn --chdir code -w 5 -b 0.0.0.0:8000 page_analyzer:app

setup:
	rm -rf .venv
	uv sync

build:
	./build.sh
	
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
