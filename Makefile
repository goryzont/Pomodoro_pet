.DEFAULT_GOAL := help
HOST=localhost
PORT=8000

run:
	poetry run gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 -c infra/gunicorn_conf.py


install:
	@echo 'Install dependency ${LIBRARY}'
	poetry add ${LIBRARY}

uninstall:
	echo 'Uninstalling dependency ${LIBRARY}'
	poetry remove ${LIBRARY}