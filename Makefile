deploy-pypi:
	python setup.py check
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload dist/*

test-pypi:
	python setup.py check
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload -r testpypi dist/*

create-docs:
	cd docs
	sphinx-apidoc -o docs/source bgameb
	$(MAKE) -C ./docs html

release:
	@read -p "Enter final version as X.Y.Z:" bump; \
	python -m incremental.update bgameb --newversion=$$bump; \
	towncrier build --yes; \
	git status