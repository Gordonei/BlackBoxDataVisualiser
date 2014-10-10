#!/usr/bin/env python
import sys
import numpy, matplotlib.pyplot as plt

def Read(filename,strip_whitespace=True,row_separator='\n',col_separator=','):
    #Reading data in from file
    datafile = open(filename,"r")
    raw_data = datafile.read().split(row_separator)
    if(strip_whitespace): raw_data = filter(None,raw_data)
    
    #Title is first line, Headers are the second
    title = raw_data[0].strip(col_separator)
    headers = raw_data[1].split(col_separator)
    
    #Turning data in numpy array
    if(strip_whitespace): data = [tuple(filter(None,d.split(col_separator))) for d in raw_data[2:]]
    else: data = [tuple(d.split(col_separator)) for d in raw_data[2:]]
    
    #Adding the headers to the datafile
    number_formats = []
    for col in numpy.array(data).transpose():
        try:
            col.astype(numpy.float)
            number_formats.append("d")
        except: number_formats.append("a")
        
    datatypes = []
    for dt,nf in zip(headers,number_formats): datatypes.append((dt,nf))
    
    data = numpy.array(data,dtype=datatypes)
    
    return (title,data)
    
def Plot(data_tuples):
    for dt in data_tuples:
        title = dt[0]
        data = dt[1]
        
        for dtype in data.dtype: print dtype[0]
        
    plt.show()

if __name__ == '__main__':
    if(len(sys.argv)>1):
        data_tuples = []
        for filename in sys.argv[1:]: data_tuples.append(Read(filename))
        
        Plot(data_tuples)
    
    else:
        print "usage: BlackBoxDataVisualiser [data file 1] [data file 2] ... [data file n]"