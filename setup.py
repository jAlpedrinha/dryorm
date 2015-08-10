from setuptools import setup, find_packages
from io import open

setup(
    name='DRY-orm',
    version='0.0.2',
    author='Jorge Alpedrinha Ramos',
    author_email='jalpedrinharamos@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    description='DRY is inspired by Django-ORM',
    long_description=open('README.rst').read(),
    install_requires=[
        'psycopg2'
    ],
)
