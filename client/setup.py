import uuid

from pip.req import parse_requirements
from setuptools import find_packages, setup

requirements = [str(r.req) for r in parse_requirements("requirements.txt", session=uuid.uuid1())]

# https://pythonhosted.org/setuptools/setuptools.html

setup(name="bdss_client",
      version="0.1",
      description="",
      classifiers=[
          "Development Status :: 1 - Planning",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.5",
          "Topic :: Communications",
          "Topic :: Scientific/Engineering"
      ],
      url="http://github.com/feltus/BDSS",
      author="Alex Feltus",
      author_email="ffeltus@clemson.edu",
      install_requires=requirements,
      packages=find_packages(),
      package_data={
          "": ["*.cfg", "*.md", "*.rst", "*.txt"]
      },
      entry_points={
          "console_scripts": ["bdss = client.cli:main"]
      },
      zip_safe=False)
