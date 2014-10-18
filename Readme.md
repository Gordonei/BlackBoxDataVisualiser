#Black Box Data Visualiser
Gordon Inggs
October, 2014

##Overview
This is a simple Python script/module for visualing data that has been produced in a flat format i.e. multiple files containing MxN matrix where the N columns are the features that you're interested in, and the M rows represent instances of these features. The file itself represents a grouping of these instances.

##Prequistes
Please install the most recent verions of:

* [Numpy](http://www.numpy.org/)
* [Matplotlib](http://matplotlib.org/)

##Installation
One of these alternatives:

* Run `python setup.py install` to install it for your Python distribution.
* Add the path to this module to your `PYTHONPATH` environmental variable, i.e. `export PYTHONPATH=$PYTHONPATH:$(pwd)` if you're in the directory that contains the module

##Usage
* Simply run `BlackBoxDataVisualiser (data file 1) (data file 2) ... (data file n)`