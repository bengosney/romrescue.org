.PHONY := install, help, update, postgres-docker
.DEFAULT_GOAL := install

INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

DB_DOCKER=rom-postgres
DB_USER=romuser
DB_PASS=rompass
DB_NAME=romdb

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.txt: requirements.%.in requirements.txt
	@echo "Builing $@"
	@pip-compile -q -o $@ $<
	@touch $@

requirements.txt: requirements.in
	@echo "Builing $@"
	@pip-compile -q $^

install: requirements.txt $(REQS) ## Install development requirements
	@echo "Installing $^"
	@pip-sync $^

$(HOOKS):
	pre-commit install

pre-init:
	pip install wheel pip-tools

init: .envrc pre-init install $(HOOKS) ## Initalise a dev enviroment
	@echo "Read to dev"
	@which direnv > /dev/null || echo "direnv not found but recommended"

update:
	@echo "Upgrading"
	pip-compile --upgrade requirements.in $(REQS)

.envrc: runtime.txt Makefile
	@echo > $@
	@echo layout python $(shell cat $^ | tr -d "-" | egrep -o "python[0-9]\.[0-9]+") >> $@
	@echo export DATABASE_URL="postgres://$(DB_USER):$(DB_PASS)@localhost:5432/$(DB_NAME)" >> $@
	@cat $@
	@echo
	@direnv allow
	@touch $@

postgres-docker: .envrc
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
