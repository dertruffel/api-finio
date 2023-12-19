
# Containers ids
postgres-id=$(shell docker ps -a -q -f "name=finio-postgres")
django-id=$(shell docker ps -a -q -f "name=finio-django")
pgadmin-id=$(shell docker ps -a -q -f "name=finio-pgadmin")


# Build docker containers
build: build-django build-postgres
build-django:
	@docker-compose -f docker-compose.yml build finio-django

build-postgres:
	@docker-compose -f docker-compose.yml build finio-postgres


build-pgadmin:
	@docker-compose -f docker-compose.yml build finio-pgadmin

# Start docker containers
start-all:
	@docker-compose up

# Stop docker containers
stop-all:
	@docker-compose stop
stop-postgres:
	-@docker stop $(postgres-id)
stop-django:
	-@docker stop $(django-id)


# Remove docker containers
rm-all: rm-django rm-postgres
rm-postgres:
	-@docker rm $(postgres-id)
rm-django:
	-@docker rm $(django-id)

# Remove, build and run docker containers
rm-build: stop-all rm-all build run
rm-build-postgres: stop-postgres rm-postgres build-postgres
rm-build-django: stop-django rm-django build-django

# Run docker containers
run:
	@docker-compose -f docker-compose.yml up

run-django:
	@docker-compose -f docker-compose.yml up finio-django


# Go to container bash shell
shell: shell-django

shell-django:
	@docker exec -it finio-django bash

shell-postgres:
	@docker exec -it finio-postgres bash


# Django commands
manage:
	@docker exec -t finio-django python src/manage.py $(cmd)

migrate:
	@docker exec -t finio-django python src/manage.py migrate

migrations:
	@docker exec -it finio-django python src/manage.py makemigrations

migrations_merge:
	@docker exec -it finio-django python src/manage.py makemigrations --merge

superuser:
	@docker exec -it finio-django python src/manage.py createsuperuser

populatedb:
	@docker exec -it finio-django python src/manage.py populatedb

# Tests
test:
	@docker exec -t finio-django /bin/sh -c "cd src && PYTHONDONTWRITEBYTECODE=1 coverage run -m pytest $(dir) --disable-warnings"

coverage:
	@docker exec -t finio-django /bin/sh -c "cd src && coverage report"

coverage-html:
	@docker exec -t finio-django /bin/sh -c "cd src && coverage html"

lint:
	@docker exec -t finio-django /bin/sh -c "cd src && flake8"

test-v:
	@docker exec -t finio-django /bin/sh -c "cd src && PYTHONDONTWRITEBYTECODE=1 coverage run -m pytest $(dir) --disable-warnings -vv"

test-v-warning:
	@docker exec -t finio-django /bin/sh -c "cd src && PYTHONDONTWRITEBYTECODE=1 coverage run -m pytest $(dir) -vv"


