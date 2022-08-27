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

release:
	@read -p "Enter final version as X.Y.Z:" bump; \
	python -m incremental.update bgameb --newversion=$$bump; \
	git add .; \
	towncrier build --yes; \
	git add .; \
	git status