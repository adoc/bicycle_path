import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    ]

setup(name='bicycle',
      version='0.1',
      description='Standard Playing Card Primitives, Games, Strategy and "AI".',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='adoc',
      author_email='adoc@code.webmob.net',
      url='https://github.com/adoc',
      keywords='',
      packages=['bicycle'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="tests",
      )
