SHELL := /bin/bash
########################################################################################################################
##
## Makefile for managing project
##
########################################################################################################################
THIS_FILE := $(lastword $(MAKEFILE_LIST))
activate = VIRTUAL_ENV_DISABLE_PROMPT=true . .venv/bin/activate;
env?=dev
docker_tag?= dev

ensure-venv:
ifeq ($(wildcard .venv),)
	@$(MAKE) -f $(THIS_FILE) venv
endif

venv:
	if [ -d .venv ]; then rm -rf .venv; fi
	python3.8 -m venv .venv --clear
	$(activate) pip3 install --upgrade pip

init: ensure-venv
	$(activate) pip3 install -r requirements.txt


fire:
	$(activate) python3.8 -m app ./data.csv ./data.json

#Docker
up:
	$(activate) docker-compose $(compose_files) up -d

down:
	$(activate) docker-compose down --remove-orphans

compose-build:
	$(activate) docker-compose build

#tests
behave:
	$(activate) docker-compose pull
	$(activate) docker-compose build
	$(activate) docker-compose up -d
	sleep 10
	$(activate) behave --junit --junit-directory=reports/tests/behave features
	$(activate) docker-compose down

e2e:
	$(activate) behave --junit --junit-directory=reports/tests/behave/ features

pylint:
	$(activate) pylint --rcfile=pylint.rc app

mypy:
	rm -rf reports/mypy-reports
	$(activate) mypy app --html-report ./reports/mypy-reports --xslt-html-report ./reports/mypy-reports

coverage:
	rm -rf reports/tests/
	mkdir -p reports/tests/coverage/ reports/tests/junit/ reports/tests/pylint/
	$(activate) coverage run --source app --module pytest -rxs -v --junit-xml=reports/tests/junit/unit_test_report.xml
	$(activate) coverage html ; mv htmlcov reports/tests/coverage
	$(activate) pylint --rcfile=pylint.rc app --output-format=parseable > reports/tests/pylint/pylint.log || true


#Terraform
terraform-up:
	$(MAKE) -C terraform/deployments/dev terraform  args="-auto-approve" env="$(env)"

terraform-account:
	$(MAKE) -C terraform/deployments/account terraform  args="-auto-approve" env="$(env)"

terraform-destroy:
	$(MAKE) -C terraform/deployments/dev terraform-destroy  args="-auto-approve"  env=$(env)

terrafile:
	$(MAKE) -C terraform/deployments/_shared terrafile args="$(args)"

