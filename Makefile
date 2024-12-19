-include env.fastapi-mongo
export $(shell sed 's/=.*//' env.fastapi-mongo )

runargs :=

.DEFAULT_GOAL := help

SERVICE_NAME := fastapi-mongo

SOURCE_DIR ?= /app
SAMPLE_PROJECT_NAME := project_sample

USERNAME ?= admin
EMAIL ?= admin@admin.com

dc := docker compose
dr := $(dc) run --rm $(SERVICE_NAME)


SHELL:=bash

OSFLAG :=
ifeq ($(OS),Windows_NT)
	OSFLAG += WIN32
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		OSFLAG += LINUX
	endif
	ifeq ($(UNAME_S),Darwin)
		OSFLAG += OSX
	endif
endif

.PHONY: poetry
poetry: ## POETRY: Run poetry commands in the source directory
	@poetry --directory ./source $(filter-out $@,$(MAKECMDGOALS))

# "Хак" для обработки аргументов после poetry
%:
	@:


.PHONY: build
build-app: ## BUILD: Build project containers and run it
	@printf "$$BGreen Build containers (time for a coffee break ☕ !) $$ColorOff \n"
	$(dc) up -d --build

.PHONY: up
up: ## RUN: Run Django containers
	@printf "$$BGreen Starting containers! $$ColorOff \n"
	$(dc) up -d

.PHONY: stop
stop: ## RUN: STOP containers
	@printf "$$BGreen Stopping containers containers! $$ColorOff \n"
	$(dc) stop

.PHONY: restart
restart: ## RUN: restart containers
	@printf "$$BGreen Restarting containers containers (time for a coffee break ☕ !) $$ColorOff \n"
	$(dc) stop
	@printf "$$BGreen Containers stopped! $$ColorOff \n"
	$(dc) up -d
	@printf "$$BGreen Containers running! $$ColorOff \n"

.PHONY: generate-keys
generate-keys:
	@mkdir -p source/certs
	@printf "\033[1;33mGenerating keys for access tokens...\033[0m\n"
	@openssl genrsa -out source/certs/jwt-private.pem 2048
	@openssl rsa -in source/certs/jwt-private.pem -outform PEM -pubout -out source/certs/jwt-public.pem
	@printf "\033[1;32mAccess token keys generated.\033[0m\n"

	@printf "\033[1;33mGenerating keys for refresh tokens...\033[0m\n"
	@openssl genrsa -out source/certs/jwt-private-refresh.pem 2048
	@openssl rsa -in source/certs/jwt-private-refresh.pem -outform PEM -pubout -out source/certs/jwt-public-refresh.pem
	@printf "\033[1;32mRefresh token keys generated.\033[0m\n"