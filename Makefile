APP = TODO_LIST

test:
	@pytest -v --disable-warnings

compose:
	@docker-compose build
	@docker-compose up