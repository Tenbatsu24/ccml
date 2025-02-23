#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_VERSION = {{ cookiecutter.python_version_number }}
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


{% if cookiecutter.dependency_file != 'none' %}
## Install Python Dependencies
.PHONY: requirements
requirements:
	{% if "requirements.txt" == cookiecutter.dependency_file -%}
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	{% elif "environment.yml" == cookiecutter.dependency_file -%}
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune
	{% elif "Pipfile" == cookiecutter.dependency_file -%}
	pipenv install
	{% endif %}
{% endif %}


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 {{ cookiecutter.module_name }}
	black --check --config pyproject.toml {{ cookiecutter.module_name }}


## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml {{ cookiecutter.module_name }}


{% if cookiecutter.environment_manager != 'none' %}
## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	{% if cookiecutter.environment_manager == 'conda' -%}
	{% if cookiecutter.dependency_file != 'environment.yml' %}
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	{% else -%}
	conda env create --name $(PROJECT_NAME) -f environment.yml
	{% endif %}
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'virtualenv' -%}
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'pipenv' -%}
	pipenv --python $(PYTHON_VERSION)
	@echo ">>> New pipenv created. Activate with:\npipenv shell"
	{% endif %}
{% endif %}


## Activate python environment
.PHONY: activate_environment
activate_environment:
	{% if cookiecutter.environment_manager == 'conda' -%}
	conda activate $(PROJECT_NAME)
	{% elif cookiecutter.environment_manager == 'virtualenv' -%}
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; workon $(PROJECT_NAME); else workon.bat $(PROJECT_NAME); fi"
	{% elif cookiecutter.environment_manager == 'pipenv' -%}
	pipenv shell
	{% endif %}


.PHONY: env
env: create_environment activate_environment requirements


.PHONY: setup_hooks
setup_hooks:
	@if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then \
		pre-commit install; \
		pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks; \
		nbautoexport install; \
		nbautoexport configure notebooks --overwrite; \
	else \
		echo "Not inside a Git repository. Skipping pre-commit setup."; \
	fi


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

{% if cookiecutter.include_code_scaffold == 'Yes' %}
## Make Dataset
.PHONY: data
data:
	$(PYTHON_INTERPRETER) {{ cookiecutter.module_name }}/dataset.py
{% endif %}

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
