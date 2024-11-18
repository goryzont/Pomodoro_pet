.DEFAULT_GOAL := help
HOST=localhost
PORT=8000

run:
	poetry run gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


install:
	@echo 'Install dependency ${LIBRARY}'
	poetry add ${LIBRARY}

uninstall:
	echo 'Uninstalling dependency ${LIBRARY}'
	poetry remove ${LIBRARY}