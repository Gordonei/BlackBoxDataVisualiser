#!/usr/bin/env python

from distutils.core import setup

from setuptools import setup
from setuptools.command.install import install
import sys


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print "Setting Path Variable"
        sys.path.append('%s:%s'%(sys.path,sys.prefix))
        install.run(self)

setup(name='BlackBoxDataVisualiser',
      version='1.0',
      description='Black Box Data Visualiser',
      author='Gordon Inggs',
      author_email='gordon.inggs@gmail.com',
      url='https://github.com/Gordonei/BlackBoxDataVisualiser',
      py_modules=['BlackBoxDataVisualiser'],
      cmdclass={
        'install': CustomInstallCommand,
      }
     )