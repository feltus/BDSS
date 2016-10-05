# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import os
import re
import uuid

from pip.req import parse_requirements
from setuptools import find_packages, setup

requirements = [str(r.req) for r in parse_requirements("requirements.txt", session=uuid.uuid1())]

# https://pythonhosted.org/setuptools/setuptools.html

# Load version from client/version.py
with open(os.path.join("client", "version.py"), "r") as version_fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', version_fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError("Unable to find version number")

# Load README from file. Convert from Markdown to RST
try:
    readme = open("../README.rst", "r").read()
except:
    raise RuntimeError("Unable to read and convert ../README.md")

setup(name="bdss_client",
      version=version,
      description="Big Data Smart Socket client",
      long_description=readme,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Topic :: Scientific/Engineering"
      ],
      url="https://github.com/feltus/BDSS",
      author="Alex Feltus",
      author_email="ffeltus@clemson.edu",
      maintainer="Nick Watts",
      maintainer_email="nick@nawatts.com",
      install_requires=requirements,
      license="GPLv2",
      packages=find_packages(exclude=["tests*"]),
      data_files=[
          ("client", ["client/defaults.cfg"])
      ],
      entry_points={
          "console_scripts": ["bdss = client.__main__:main"]
      },
      zip_safe=False)
