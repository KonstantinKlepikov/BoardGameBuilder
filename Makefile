test-pypi:
	python setup.py check
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload -r testpypi dist/*

create-docs:
	python setup.py build_sphinx

release:
	@read -p "Enter final version as X.Y.Z:" bump; \
	python -m incremental.update bgameb --newversion=$$bump; \
	towncrier build --yes; \
	git status

test:
	python -m pytest -x -s -v -m "not slow"

log:
	@read -p "Enter newsfragment name:" frag; \
	towncrier create $$frag