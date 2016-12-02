#!/usr/bin/env python

import os
import re
import sys

from codecs import open

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'routes',
]

requires = []

test_requirements = ['pytest>=2.8.0', 'pytest-cov']

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='routes',
    description='Flask like routes for django',
    long_description=readme,
    author='Alex Kessinger',
    author_email='voidfiles@gmail.com',
    url='http://github.com/voidfiles/django-flask-routes',
    packages=packages,
    package_data={'': ['LICENSE', 'HISTORY.rst'], 'routes': []},
    package_dir={'routes': 'routes'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ),
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
