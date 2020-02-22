
env:
	python3 -m venv env
	./env/bin/pip install -r requirements.txt
	./env/bin/pip install -e .

test: env
	./env/bin/py.test tests/

check: env
	./env/bin/pycodestyle --exclude env .
	./env/bin/flake8 --exclude env .
	./env/bin/black --exclude env .

clean:
	find ./ -name "*.pyc" -delete
	find ./ -name "*~" -delete

push: check test
	git push origin HEAD
