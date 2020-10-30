# Makefile
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down -v

restart:
	make down
	make up
	make logs

logs:
	docker-compose logs -f

rebuild:
	make build
	make up
	make logs