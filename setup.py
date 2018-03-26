#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup


def find_subpackages(package):
    packages = [package]
    for subpackage in find_packages(package):
        packages.append("{0}.{1}".format(package, subpackage))
    return packages


setup(name="xrally-repo-init",
      version="0.0.1",
      description="Creates package skeleton for rally plugins development.",
      url="https://github.com/xrally/xrally-repo-init",
      author="xRally.org",
      author_email="boris@pavlovic.me",
      packages=find_subpackages("builder"),
      package_dir={'builder': 'builder'},
      package_data={'builder': ['skeletons/*.j2']},
      platforms='Linux',
      license='Apache 2.0',
      entry_points={
          "console_scripts": [
              "xrally-repo-init = builder.main:main"
          ]
      })
