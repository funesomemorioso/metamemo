include .env

help:	## List all make commands
	@awk 'BEGIN {FS = ":.*##"; printf "\n  Please use `make <target>` where <target> is one of:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)
	@echo ' '

build:		## Build the project with -d and --no-recreate flags
	$(DOCKER_COMPOSE) up --build --no-recreate -d

install:	## Exec container and make npm install commands
	$(DOCKER_EXEC_TOOLS_APP) -c $(NODE_INSTALL)

bundle:		## Run build npm command script
	$(DOCKER_EXEC_TOOLS_APP) -c $(BUNDLE_RUN)

clean:		## Remove all dist/ files
	$(DOCKER_EXEC_TOOLS_APP) -c $(CLEAN_RUN)

interact:	## Interact to install new packages or run specific commands in container
	$(DOCKER_EXEC_TOOLS_APP)

dev:		# Internal command to run dev npm command script
	$(DOCKER_EXEC_TOOLS_APP) -c $(SERVER_RUN)

up:		## Run up -d Docker command container will wait for interactions
	$(DOCKER_COMPOSE) up -d

start:	up dev ## Up the docker env and run the npm run dev it to

first:	build install dev ## Build the env, up it and run the npm install and then run npm run dev it to

stop:	$(ROOT_DIR)/compose.yml	## Stop and remove containers
	$(DOCKER_COMPOSE) kill
	$(DOCKER_COMPOSE) rm --force
restart:  stop start dev ## Stop and restart container

clear:	stop $(ROOT_DIR)/compose.yml ## Stop and remove container and orphans
	$(DOCKER_COMPOSE) down -v --remove-orphans
