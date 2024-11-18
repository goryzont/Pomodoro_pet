.DEFAULT_GOAL := help
HOST=localhost
PORT=8000

run:
	uvicorn main:app --host ${HOST} --port ${PORT} --reload --env-file .env

install:
	@echo 'Install dependency ${LIBRARY}'
	poetry add ${LIBRARY}

uninstall:
	echo 'Uninstalling dependency ${LIBRARY}'
	poetry remove ${LIBRARY}