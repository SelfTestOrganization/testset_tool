#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Jan Hutař",
    author_email='jhutar@seznam.cz',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Library to read and check SelfTest test set files",
    entry_points={
        'console_scripts': [
            'testset_tool=testset_tool.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='testset_tool',
    name='testset_tool',
    packages=find_packages(include=['testset_tool', 'testset_tool.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jhutar/testset_tool',
    version='0.1',
    zip_safe=False,
)
