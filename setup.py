"""Setup script."""

import os.path

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='smoothtables',
    version='1.0.0',
    description=('A module to generate tables and panels with box drawing '
                 'borders.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='~=3.6',
    author='Leandro Baca',
    author_email='leandrobaca77@gmail.com',
    url='https://github.com/lbaca/smoothtables',
    py_modules=['smoothtables'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Printing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
        'Topic :: Software Development',
    ],
    keywords='table tables panel panels text box drawing',
)
