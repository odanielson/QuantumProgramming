

clean:
	find ./ -name "*.pyc" -delete
	find ./ -name "*~" -delete

test:
	PYTHONPATH=$(PWD) py.test tests/

check:
	pep8 -r ./
	frosted -r ./
