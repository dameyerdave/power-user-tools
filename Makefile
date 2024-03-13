install:
	@python setup.py install
clean:
	@rm -rf build dist *.egg-info
build: clean
	@python3 setup.py sdist bdist_wheel
deploy: build
	@twine upload dist/*
doc:
	cd docs && $(MAKE) html
bundle:
	@scripts/bundle.sh