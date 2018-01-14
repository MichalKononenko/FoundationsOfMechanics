"""
Main setup file for the library
"""
from setuptools import setup, find_packages

setup(
    name='fom',
    version='0.1',
    description='Physics engine based on Abraham and Marsden',
    author='Michal Kononenko',
    author_email='michalkononenko@gmail.com',
    packages=find_packages(exclude=["test.*"])
)
