#########
# Tasks #
#########

.PHONY: test
test: test/run ## All-in-one command to start requirements, compile and test the application.
test/run:
	@sudo docker-compose up -d
	@sleep 3
	( \
		. $(PYTHON_BIN)/activate; \
		py.test test; \
	)
	@sudo docker-compose down

.PHONY: dev-setup
dev-setup: ## Setup the local development environment with python3 venv and project dependencies.
	sudo apt-get update
	sudo pip3 install virtualenv
	sudo apt-get install python3-dev python3-venv
	python3 -m venv .env
	( \
		. $(PYTHON_BIN)/activate; \
		 pip install --upgrade pip \
		pip install -r requirements.txt; \
	)

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
.PHONY: help
help:
	@echo "$$(tput bold)Available Tasks:$$(tput sgr0)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-5s\033[0m %s\n", $$1, $$2}'


###############
# Definitions #
###############

PYTHON_BIN ?= .env/bin