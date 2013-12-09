import re

from distutils.core import setup

version = None
for line in open('./goodreads/__init__.py'):
    match = re.search('__version__\s*=\s*(.*)', line)
    if match:
        version = match.group(1).strip()[1::-1]
        break

assert version

setup(
    name='goodreads',
    version=version,
    description='Python wrapper to communicate with Goodreads API.',
    author='Brian Bridges',
    author_email='brian.brdgs@gmail.com',
    url='https://github.com/GrumpyRainbow/goodreads-py',
    packages=['goodreads'],
    tests_require=[
        'nose>=1.1.2',
    ],
    test_suite='nose.collector',
)
