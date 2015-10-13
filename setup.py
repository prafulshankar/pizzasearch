from setuptools import setup, find_packages


setup(
    name = "pizzasearch",
    version = "0.1dev",
    packages = ['pizza','piazza_api2'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description = open('README.md').read(),
    author = "Praful Shankar",
    author_email = "praful.shankar@berkeley.edu",
    url = "https://github.com/prafulshankar/pizzasearch",
    download_url="https://github.com/prafulshankar/pizzasearch/tarball/0.1dev",
    install_requires=[
      'html2text', 'requests'
    ],
    entry_points = {
        'console_scripts': ['pizza=pizza.pizza:main'],
    }
)