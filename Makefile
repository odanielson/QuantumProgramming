

clean:
	find ./ -name "*.pyc" -delete
	find ./ -name "*~" -delete


check:
	pep8 -r ./
	frosted -r ./
