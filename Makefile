VENV := .venv

CI_BRANCH := $(shell git branch | grep \* | cut -d ' ' -f2)
CI_COMMIT_ID := $(shell git rev-parse HEAD)

clean_venv:
	source deactivate || true
	rm -rf $(VENV)

clean_env:
	rm -f .env

env: clean_env
	cp -p .env.tpl .env

$(VENV): clean_venv
	command -v deactivate && source deactivate || true
	python -m venv $(VENV)
	source $(VENV)/bin/activate && pip install --upgrade pip~=21.3 pip-tools

requirements.txt: requirements.in
	test -r $(VENV) || make $(VENV)
	source $(VENV)/bin/activate \
	&& pip-compile --no-emit-index-url --output-file requirements.txt requirements.in

setup:
	test -r $(VENV) || make $(VENV)
	test -r .env || make env
	test -f requirements.txt || make requirements.txt
	source $(VENV)/bin/activate && pip install -r requirements.txt

pip_sync: requirements.txt
	source $(VENV)/bin/activate && pip-sync requirements.txt

runserver:
	test -r .env || make env
	CI_BRANCH=$(CI_BRANCH) \
	CI_COMMIT_ID=$(CI_COMMIT_ID) \
	$(VENV)/bin/uvicorn app.server:app --host 0.0.0.0 --port 9080 --reload

spec=test
runtest:
	source $(VENV)/bin/activate \
	&& PYTHONDONTWRITEBYTECODE=1 $(VENV)/bin/pytest -vvv '${spec}'
