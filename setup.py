#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click==7.0', 'slackclient==2.1.0']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="evan",
    author_email='cppmain@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    description="jy answer interesting thing",
    entry_points={
        'console_scripts': [
            'jy=bot.jy:main',
        ]
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='jy',
    name='jy-bot',
    packages=find_packages(include=['bot']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lanen/jy-bot',
    version='1.0.0',
    zip_safe=False,
)
