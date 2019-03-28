.DEFAULT_GOAL := default_target
.PHONY: default_target test clean setup create-venv setup-dev setup-os git-up git-add-migrations migrations translate-up translate-compile migrations-up migrations-clean migrations-from-scratch db-up code-convention test run all

NPROC := `grep -c ^processor /proc/cpuinfo`

# https://github.com/pytest-dev/pytest/issues/4101
PYTEST := py.test -n$(NPROC)

PIP := pip install -r

GITLAB_RUNNER := gitlab-ci-multi-runner exec docker

ADMIN_URL := `openssl rand -base64 48`
SECRET_KEY := `bash utility/generate-secret-key.sh`

PROJECT_NAME := life-insurance-bank
PYTHON_VERSION := 3.6.6
VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)


# Environment setup
.pip:
	pip install pip --upgrade

setup-dev: .pip
	$(PIP) requirements.txt

setup-os:
	bash utility/install-docker.sh
	bash utility/install-gitlab-runner.sh

.clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/

clean: .clean-build .clean-pyc .clean-test ## remove all build, test, coverage and Python artifacts

.create-venv:
	pyenv install -s $(PYTHON_VERSION)
	pyenv uninstall -f $(VENV_NAME)
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	pyenv local $(VENV_NAME)

create-venv: .create-venv setup-dev

# Repository
git-up:
	git pull
	git fetch -p --all

code-convention:
	flake8
	pycodestyle

# Tests
test:
	py.test --cov-report=term-missing  --cov-report=html --cov=.

job-test:
	$(GITLAB_RUNNER) "unit test"

# Server
run:
	DJANGO_READ_DOT_ENV_FILE=on python manage.py runserver 0.0.0.0:8000


all: create-venv git-up setup-dev default_target

default_target: clean collectstatic code-convention test
