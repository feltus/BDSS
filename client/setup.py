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
import uuid

from pip.req import parse_requirements
from setuptools import find_packages, setup

requirements = [str(r.req) for r in parse_requirements("requirements.txt", session=uuid.uuid1())]

# https://pythonhosted.org/setuptools/setuptools.html

# Load version from client/version.py
exec(open(os.path.join("client", "version.py")).read())

setup(name="bdss_client",
      version=__version__,  # noqa
      description="",
      classifiers=[
          "Development Status :: 1 - Planning",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.5",
          "Topic :: Communications",
          "Topic :: Scientific/Engineering"
      ],
      url="http://github.com/feltus/BDSS",
      author="Alex Feltus",
      author_email="ffeltus@clemson.edu",
      install_requires=requirements,
      license="GPLv2",
      packages=find_packages(),
      package_data={
          "": ["*.cfg", "*.md", "*.rst", "*.txt"]
      },
      entry_points={
          "console_scripts": ["bdss = client.__main__:main"]
      },
      zip_safe=False)
