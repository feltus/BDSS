# Publish an Update to PyPI

See [Python Packaging User Guide](https://packaging.python.org/distributing) for more information.

## Requirements

* Configure [`$HOME/.pypirc`](https://docs.python.org/3/distutils/packageindex.html#pypirc)
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

## Test published package

* Create an account on [Test PyPI](https://testpypi.python.org/pypi).
* Configure `$HOME/.pypirc` with the Test PyPI index:
  ```
  [distutils]
  index-servers =
      pypi
      testpypi

  [pypi]
  repository = https://pypi.python.org/pypi
  username = $USERNAME

  [testpypi]
  repository = https://testpypi.python.org/pypi
  username = $USERNAME
  ```
  Replace `$USERNAME` with your Test PyPI username.
* Follow normal steps to publish except when uploading with Twine, run `twine upload --repository testpypi`
* Install package from Test PyPI (in another virtualenv).
  ```
  pip install --index-url https://testpypi.python.org/simple --extra-index-url https://pypi.python.org/simple bdss-client
  ```
  The extra index URL pointing to production PyPI is necessary for installing dependencies of BDSS.
* Check that `bdss` is installed and working. `bdss -h`
