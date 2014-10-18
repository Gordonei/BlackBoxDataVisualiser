#Black Box Data Visualiser
Gordon Inggs
October, 2014

##Overview
This is a simple Python script/module for visualing data that has been produced in a flat format i.e. multiple files containing MxN matrix where the N columns are the features that you're interested in, and the M rows represent instances of these features. The file itself represents a grouping of these instances.

##Prequistes
Please install the most recent versions of:

* [Numpy](http://www.numpy.org/)
* [Matplotlib](http://matplotlib.org/)

##Installation
* Run `python setup.py install` in the unpacked directory to install it

##Usage
* Simply run `BlackBoxDataVisualiser (data file 1) (data file 2) ... (data file n)` from the command line

Or

* Import as a Python module i.e. `import BlackBoxDataVisualiser` or e.g.

```python
import BlackBoxDataVisualiser

filename = "path/to/your/file"
data_dict = Read(filename)

Plot(data_dict)
```
