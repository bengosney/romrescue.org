.PHONY := install, help, update, postgres-docker
.DEFAULT_GOAL := install

REQS=$(shell python -c 'import tomllib;[print(f"requirements.{k}.txt") for k in tomllib.load(open("pyproject.toml", "rb"))["project"]["optional-dependencies"].keys()]')

DB_DOCKER=rom-postgres
DB_USER=romuser
DB_PASS=rompass
DB_NAME=romdb

BINPATH=$(shell which python | xargs dirname | xargs realpath --relative-to=".")
PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
PIP_PATH:=$(BINPATH)/pip
WHEEL_PATH:=$(BINPATH)/wheel
PRE_COMMIT_PATH:=$(BINPATH)/pre-commit
UV_PATH:=$(BINPATH)/uv

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile --extra $* $(filter-out $<,$^) > $@

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile $(filter-out $<,$^) > $@

$(PIP_PATH):
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@

$(WHEEL_PATH): $(PIP_PATH)
	python -m pip install wheel
	@touch $@

$(UV_PATH): $(PIP_PATH) $(WHEEL_PATH)
	python -m pip install uv
	@touch $@

$(HOOKS):
	pre-commit install

install: python

python: $(UV_PATH) requirements.txt $(REQS)
	@echo "Installing $(filter-out $<,$^)"
	@python -m uv pip sync $(filter-out $<,$^)

init: .direnv requirements.txt requirements.dev.txt $(HOOKS) ## Initalise a dev enviroment
	@echo "Read to dev"
	@which direnv > /dev/null || echo "direnv not found but recommended"

.direnv: .envrc
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools
	@touch $@ $^

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.10" > $@
	@echo export DATABASE_URL="postgres://$(DB_USER):$(DB_PASS)@localhost:5432/$(DB_NAME)" >> $@
	@touch -d '+1 minute' $@
	@false

postgres-docker: .direnv
	@docker stop $(DB_DOCKER) || true
	docker run --rm --name $(DB_DOCKER) -p 5432:5432 -e POSTGRES_PASSWORD=$(DB_PASS) -e POSTGRES_USER=$(DB_USER) -e POSTGRES_DB=$(DB_NAME) -d postgres

latest.dump:
	heroku pg:backups:capture
	heroku pg:backups:download

import-db: latest.dump
	export "PGPASSWORD=$(DB_PASS)" && pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $(DB_USER) -d $(DB_NAME) $^

clean:
	rm -f latest.dump

shrink:
	heroku run 'python manage.py thumbnail_cleanup'
	heroku run 'python manage.py clean_dogs'
	heroku run 'python manage.py clearsessions'
