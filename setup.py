#!/usr/bin/env python

from setuptools import setup
from codecs import open

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name = 'networth',
    version = '0.8.0',
    author = 'Ken Kundert',
    author_email = 'networth@nurdletech.com',
    description = 'Summarize net worth',
    long_description = readme,
    url = 'https://github.com/kenkundert/networth',
    download_url = 'https://github.com/kenkundert/networth/tarball/master',
    license = 'GPLv3+',
    scripts = 'networth'.split(),
    install_requires = [
        'appdirs',
        'arrow',
        'avendesora>=1.12',
        'docopt',
        'inform>=1.14',
        'nestedtext',
        'python-gnupg>=0.4.3',
            # Be careful.  There's a package called 'gnupg' that's an 
            # incompatible fork of 'python-gnupg'.  If both are installed, the 
            # user will probably have compatibility issues.
        'quantiphy',
        'quantiphy_eval>=0.3',
        'voluptuous',
    ],
    python_requires='>=3.6',
    keywords = 'networth'.split(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
)
