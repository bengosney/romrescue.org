.PHONY := install, install-dev, help, update, postgres-docker
.DEFAULT_GOAL := install-dev

INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

DB_DOCKER=rom-postgres
DB_USER=romuser
DB_PASS=rompass
DB_NAME=romdb

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.txt: requirements.%.in
	@echo "Builing $@"
	@pip-compile -q -o $@ $^

requirements.txt: requirements.in
	@echo "Builing $@"
	@pip-compile -q $^

update:
	@echo "Upgrading"
	pip-compile --upgrade requirements.in $(REQS)

install: requirements.txt ## Install production requirements
	@echo "Installing $^"
	@pip-sync $^

install-dev: requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $^"
	@pip-sync $^

runtime.txt:
	@echo "python-3.8.6" > $@

.envrc: runtime.txt Makefile
	@echo > $@
	@echo layout python $(shell cat $^ | tr -d "-" | egrep -o "python[0-9]\.[0-9]") >> $@
	@echo export DATABASE_URL="postgres://$(DB_USER):$(DB_PASS)@localhost:5432/$(DB_NAME)" >> $@
	@cat $@
	@echo
	@direnv allow
	@touch $@

postgres-docker: .envrc
	@docker stop $(DB_DOCKER) || true
	docker run --rm --name $(DB_DOCKER) -p 5432:5432 -e POSTGRES_PASSWORD=$(DB_PASS) -e POSTGRES_USER=$(DB_USER) -e POSTGRES_DB=$(DB_NAME) -d postgres
