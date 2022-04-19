.PHONY: clean clean-model clean-pyc docs help init build-docker create-container start-container jupyter test lint profile clean clean-data clean-docker clean-container clean-image sync-from-source sync-to-source
.DEFAULT_GOAL := help

###########################################################################################################
## SCRIPTS
###########################################################################################################

define PRINT_HELP_PYSCRIPT
import os, re, sys

if os.environ['TARGET']:
    target = os.environ['TARGET']
    is_in_target = False
    for line in sys.stdin:
        match = re.match(r'^(?P<target>{}):(?P<dependencies>.*)?## (?P<description>.*)$$'.format(target).format(target), line)
        if match:
            print("target: %-20s" % (match.group("target")))
            if "dependencies" in match.groupdict().keys():
                print("dependencies: %-20s" % (match.group("dependencies")))
            if "description" in match.groupdict().keys():
                print("description: %-20s" % (match.group("description")))
            is_in_target = True
        elif is_in_target == True:
            match = re.match(r'^\t(.+)', line)
            if match:
                command = match.groups()
                print("command: %s" % (command))
            else:
                is_in_target = False
else:
    for line in sys.stdin:
        match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
        if match:
            target, help = match.groups()
            print("%-20s %s" % (target, help))
endef

define START_DOCKER_CONTAINER
if [ `$(DOCKER) inspect -f {% raw -%}{{.State.Running}}{%- endraw %} $(CONTAINER_NAME)` = "false" ] ; then
        $(DOCKER) start $(CONTAINER_NAME)
fi
endef

###########################################################################################################
## VARIABLES
###########################################################################################################

{%- if cookiecutter.use_nvidia_docker == 'yes' %}
export DOCKER=nvidia-docker
{%- else %}
export DOCKER=docker
{%- endif %}
export TARGET=
export PWD=`pwd`
export PRINT_HELP_PYSCRIPT
export START_DOCKER_CONTAINER
export PYTHONPATH=$PYTHONPATH:$(PWD)
export project_slug={{ cookiecutter.project_slug }}
export IMAGE_NAME=$(project_slug)-image
export CONTAINER_NAME=$(project_slug)-container
export DATA_SOURCE={{ cookiecutter.data_source }}
export JUPYTER_HOST_PORT={{ cookiecutter.jupyter_host_port }}
export JUPYTER_CONTAINER_PORT=8888
export PYTHON=python3
export DOCKERFILE=docker/Dockerfile

###########################################################################################################
## ADD TARGETS SPECIFIC TO "{{ cookiecutter.project_slug }}"
###########################################################################################################


###########################################################################################################
## GENERAL TARGETS
###########################################################################################################

help: ## show this message
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

init: build-docker sync-from-source ## initialize repository for traning

sync-from-source: ## download data data source to local envrionment
{%- if cookiecutter.data_source_type == 's3' %}
	-aws s3 sync $(DATA_SOURCE) ./data/
{%- elif cookiecutter.data_source_type == 'url' %}
	wget $(DATA_SOURCE) -P ./data/
{% endif %}


build-docker: ## build docker `release` image
	$(DOCKER) build -t $(IMAGE_NAME) -f $(DOCKERFILE) --build-arg UID=$(shell id -u) .
	$(DOCKER) system prune

# To use this target you will execute it as the following #
# make -e stage=test build-docker-stage
STAGE = test 
build-docker-target: ## build any stage in the Dockerfile's alias name
	$(DOCKER) build --target $(STAGE) -f $(DOCKERFILE) --build-arg UID=$(shell id -u) .

build-docker-no-cache: ## initialize docker image without cachhe
	$(DOCKER) build --no-cache -t $(IMAGE_NAME) -f $(DOCKERFILE) --build-arg UID=$(shell id -u) .

sync-to-source: ## sync local data to data source
{%- if cookiecutter.data_source_type == 's3' %}
	-aws s3 sync ./data/ $(DATA_SOURCE)
{%- elif cookiecutter.data_source_type == 'url' %}
	echo "no sync target for url data source..."
{% endif %}

create-container: ## create docker container
	$(DOCKER) run --rm -it -v $(PWD):/app --name $(CONTAINER_NAME) $(IMAGE_NAME)

start-container: ## start docker container
	@echo "$$START_DOCKER_CONTAINER" | $(SHELL)
	@echo "Launched $(CONTAINER_NAME)..."
	$(DOCKER) attach $(CONTAINER_NAME)

jupyter: ## start Jupyter Notebook server
	jupyter-notebook --ip=0.0.0.0 --port=${JUPYTER_CONTAINER_PORT}

install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install	
	@poetry shell

format: ## Format code using isort and black.
	@echo "🚀 Formatting code: Running isort and black"
	@isort .
	@black .

lint: ## Check code formatting using isort and black.
	@echo "🚀 Checking code formatting: Running isort and black"
	@isort --check-only --diff .
	@black --check .

test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@pytest --doctest-modules

build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

clean-build: ## clean build artifacts
	@rm -rf dist

{%- if cookiecutter.mkdocs == "y" %}

docs-test: ## Test if documentation can be built without warnings or errors
	@mkdocs build -s

docs: ## Build and serve the documentation
	@mkdocs serve

.PHONY: docs
{%- endif %}

profile: ## show profile of the project
	@echo "project_slug: $(project_slug)"
	@echo "CONTAINER_NAME: $(CONTAINER_NAME)"
	@echo "IMAGE_NAME: $(IMAGE_NAME)"
	@echo "JUPYTER_PORT: `$(DOCKER) port $(CONTAINER_NAME)`"
	@echo "DATA_SOURE: $(DATA_SOURCE)"

clean: clean-model clean-pyc clean-docker ## remove all artifacts

clean-model: ## remove model artifacts
	rm -fr model/*

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

distclean: clean clean-data ## remove all the reproducible resources including Docker images

clean-data: ## remove files under data
	rm -fr data/*

clean-docker: clean-container clean-image ## remove Docker image and container

clean-container: ## remove Docker container
	-$(DOCKER) rm $(CONTAINER_NAME)

clean-image: ## remove Docker image
	-$(DOCKER) image rm $(IMAGE_NAME)

prune-image: ## prune dangleing images
	-$(DOCKER) system prune
