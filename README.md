# BoardGameBuilder

Object-oriented framework for build boardgame logic on python

`pip install bgameb`

## Development

`pip install bgameb[dev]`. Use ipython for development from env: `python -m IPython`

### Build the docs

`make create-docs`

### Changelog

`towncrier create 123.feature`

[towncrier](https://pypi.org/project/towncrier/)

> .feature: Signifying a new feature.
> .bugfix: Signifying a bug fix.
> .doc: Signifying a documentation improvement.
> .removal: Signifying a deprecation or removal of public API.
> .misc: A ticket has been closed, but it is not of interest to users.
> .cicd: Integration tasks

### Release

Test send to pypi: `make test-pypi`

- stage diffs
- `towncrier build --draft`
- `make release`
