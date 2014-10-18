#!/usr/bin/env python

from distutils.core import setup

from setuptools import setup
from setuptools.command.install import install

setup(name='BlackBoxDataVisualiser',
      version='1.0',
      description='Black Box Data Visualiser',
      author='Gordon Inggs',
      author_email='gordon.inggs@gmail.com',
      url='https://github.com/Gordonei/BlackBoxDataVisualiser',
      py_modules=['BlackBoxDataVisualiser'],
      scripts=['bin/BlackBoxDataVisualiser'] #This is just a symbolic link to the main module, which can run things.
     )