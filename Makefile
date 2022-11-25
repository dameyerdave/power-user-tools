install:
	@python setup.py install
clean:
	@rm -rf build dist *.egg-info
build: clean
	@python setup.py sdist bdist_wheel
deploy: build
	@twine upload dist/*
