# Publish an Update to PyPI

See [Python Packaging User Guide](https://packaging.python.org/distributing) for more information.

## Requirements

* Configure [`$HOME/.pypirc`](https://docs.python.org/3/distutils/packageindex.html#pypirc)
* Install [twine](https://pypi.python.org/pypi/twine)

## Steps to publish

* cd to client directory. `cd /path/to/bdss/client`
* Create symlink to project README. `ln -s ../README.rst README.rst`
* Update version in `client/version.py`
   * http://semver.org/
   * https://packaging.python.org/distributing/#semantic-versioning-preferred
* Create Git tag. `git tag client-v<version>`
* Remove any old builds. `rm -r ./dist`
* Build source and wheel distributions. `python setup.py sdist bdist_wheel`
* Upload using twine. `twine upload dist/*`

## Test published package

* Create an account on [TestPyPI](https://test.pypi.org/).
* Configure `$HOME/.pypirc` with the TestPyPI index:
  ```
  [distutils]
  index-servers =
      pypi
      testpypi

  [pypi]
  repository = https://upload.pypi.org/legacy/
  username = $USERNAME

  [testpypi]
  repository = https://test.pypi.org/legacy/
  username = $USERNAME
  ```
  Replace `$USERNAME` with your TestPyPI username.
* Follow normal steps to publish except when uploading with Twine, run `twine upload --repository testpypi`
* Install package from TestPyPI (in another virtualenv).
  ```
  pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple bdss-client
  ```
  The extra index URL pointing to production PyPI is necessary for installing dependencies of BDSS.
* Check that `bdss` is installed and working. `bdss -h`
