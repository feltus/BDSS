# Publish an Update to PyPI

See [Python Packaging User Guide](https://packaging.python.org/distributing) for more information.

## Requirements

* Install [Pandoc](http://pandoc.org/) and [PyPandoc](https://pypi.python.org/pypi/pypandoc/)
* Configure [`$HOME/~.pypirc`](https://docs.python.org/3/distutils/packageindex.html#pypirc)
* Install [twine](https://pypi.python.org/pypi/twine)

## Steps to publish

* Update version in `client/version.py`
   * http://semver.org/
   * https://packaging.python.org/distributing/#semantic-versioning-preferred
* Create Git tag. `git tag client-v<version>`
* cd to client directory. `cd /path/to/bdss/client`
* Remove any old builds. `rm -r ./dist`
* Build source and wheel distributions. `python setup.py sdist bdist_wheel`
* Upload using twine. `twine upload dist/*`
