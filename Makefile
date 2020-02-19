
env:
	python3 -m venv env
	./env/bin/pip install -r requirements.txt

clean:
	find ./ -name "*.pyc" -delete
	find ./ -name "*~" -delete

test: env
	PYTHONPATH=$(PWD) ./env/bin/py.test tests/

check: env
	./env/bin/pycodestyle --exclude env .
	./env/bin/flake8 --exclude env .
	./env/bin/black --exclude env .
