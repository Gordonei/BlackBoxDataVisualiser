#!/usr/bin/env python
import sys
import numpy, matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

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

def drawViewFigure(viewer_fig,data_tuples,x_label,y_label):
    viewer_fig.clear()
    viewer_ax = viewer_fig.add_subplot(111)
    
    for dt in data_tuples:
        title = dt[0]
        data = dt[1]
        viewer_ax.plot(data[x_label],data[y_label],label=title) #rather than replotting every time, maybe just change the data ranges?
        
    viewer_fig.canvas.draw()
    
def Plot(data_tuples):
    
    viewer_fig = plt.figure()
    viewer_ax = viewer_fig.add_subplot(111)
    
    x_label = 0
    y_label = 1
    
    columns = []
    for dt in data_tuples:
        data = dt[1]
        for datatype_name in data.dtype.names:
            if(datatype_name not in columns): columns.append(datatype_name)
            
    x_label = columns[x_label] #default with 1st and 2nd column
    y_label = columns[y_label]
    
    
    drawViewFigure(viewer_fig,data_tuples,x_label,y_label)
     
    controls_fig = plt.figure()
    axcolor = 'w'
    rax = plt.axes([0.05, 0.7, 0.15, 0.15], axisbg=axcolor)  
    radio = RadioButtons(rax, tuple(columns))
    
    def x_axesChange(label):
        x_label = label
        drawViewFigure(viewer_fig,data_tuples,x_label,y_label)
        
    radio.on_clicked(x_axesChange)
    
    rax = plt.axes([0.05, 0.4, 0.15, 0.15], axisbg=axcolor)
    radio2 = RadioButtons(rax, tuple(columns))
    
    def y_axesChange(label):
        y_label = label
        drawViewFigure(viewer_fig,data_tuples,x_label,y_label)
        
    radio2.on_clicked(y_axesChange)
    
    #plt.legend(loc="best")
    plt.show()

if __name__ == '__main__':
    if(len(sys.argv)>1):
        data_tuples = []
        for filename in sys.argv[1:]: data_tuples.append(Read(filename))
        
        Plot(data_tuples)
    
    else:
        print "usage: BlackBoxDataVisualiser [data file 1] [data file 2] ... [data file n]"