install:
	@python setup.py
clean:
	@rm -rf build dist *.egg-info
build:
	@python setup.py sdist bdist_wheel
deploy: build
	@twine upload dist/*
