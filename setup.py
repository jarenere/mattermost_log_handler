# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup


def readme(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='mattermost_log_handler',
    packages=['mattermost_log_handler'],

    version='0.0.1',
    author='Julio Arenere Mendoza',
    author_email='jarenere@gmail.com',
    description=('Posts log events to Mattermost via webhook'),
    long_description=readme('README.rst'),
    license='MIT',
    keywords=['mattermost', 'logging', 'handler'],
    url='https://github.com/nukru/mattermost_log_handler',
    download_url='https://github.com/nukru/mattermost_log_handler/archive/master.zip',
    include_package_data=True,
    install_requires=[
        'requests >= 2.2.1',
        ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Chat',
        'Topic :: System :: Logging'
    ]
)
