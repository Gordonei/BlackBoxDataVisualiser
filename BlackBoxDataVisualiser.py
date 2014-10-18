#!/usr/bin/env python
import sys
import numpy, matplotlib.pyplot as plt
from matplotlib.widgets import Slider,RadioButtons

def headerSnoop(raw_data,col_separator):
    """
    Helper function for trying to detect where the data file header ends and the data begins.
    """
    header_length_guess = 0
    for i,rd in enumerate(numpy.array(raw_data)):
        #This probably isn't a very Pythonic way to do this...
        try:
            numpy.array(rd.split(col_separator)[:-1]).astype(numpy.float)
            if not(header_length_guess): header_length_guess = i
        
        except(ValueError): pass
    
    return header_length_guess


def Read(filename,strip_whitespace=True,row_separator='\n',col_separator=',',header_rows=0,title_row=0):
    """
    High level function for reading in data from a flat file.
    """
    #Reading data in from file
    datafile = open(filename,"r")
    raw_data = datafile.read().split(row_separator)
    if(strip_whitespace): raw_data = filter(None,raw_data)
    
    #Title is first line, Column Headers are the last line of the header
    title = raw_data[title_row].strip(col_separator)
    
    #If header rows aren't specified, use the snooper helper function to try 
    if not(header_rows): header_rows = headerSnoop(raw_data,col_separator)
    
    headers = raw_data[header_rows-1].split(col_separator)
    
    #Turning data in numpy array
    if(strip_whitespace): data = [tuple(filter(None,d.split(col_separator))) for d in raw_data[header_rows:]]
    else: data = [tuple(d.split(col_separator)) for d in raw_data[header_rows:]]
    
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
    
    return {"title":title,"data":data}

def drawViewFigure(viewer_fig,data_dicts,x_label,y_label):
    """
    Helper function for redrawing the view window for the x and y labels.
    """
    viewer_fig.clear()
    viewer_ax = viewer_fig.add_subplot(111)
    
    for dd in data_dicts:
        title = dd["title"]
        data = dd["data"]
        if(x_label in data.dtype.names and y_label in data.dtype.names): viewer_ax.plot(data[x_label],data[y_label],label=title) #rather than replotting every time, maybe just change the data ranges?
        
    for ax in viewer_fig.axes:
        ax.set_xlabel(x_label)    
        ax.set_ylabel(y_label)
    
    viewer_fig.canvas.draw()
    
def drawAxesControls(controls_fig,viewer_fig,columns):
    axcolor = 'w'
    char_width = max(map(lambda x:len(x),columns)) #finding the widest column title
    
    #X offset, y offset, x length, y length
    rax = plt.axes([0.05, 0.1 + 0.03*len(columns) + 0.1, 0.02*char_width, 0.03*len(columns)], axisbg=axcolor,title="X Axis")  
    radio = RadioButtons(rax, tuple(columns))
    
    def x_axesChange(label):
        global x_label,y_label #Should probably do this in a more OOP way
        x_label = label
        drawViewFigure(viewer_fig,data_dicts,x_label,y_label)
        
    radio.on_clicked(x_axesChange)
    
    rax = plt.axes([0.05, 0.1, 0.02*char_width, 0.03*len(columns)], axisbg=axcolor,title="Y Axis")
    radio2 = RadioButtons(rax, tuple(columns))
    
    def y_axesChange(label):
        global x_label,y_label
        y_label = label
        drawViewFigure(viewer_fig,data_dicts,x_label,y_label)
        
    radio2.on_clicked(y_axesChange)
    
    return [radio,radio2]

#Global variables used during plotting
x_label = 0
y_label = 1
    
def Plot(data_dicts):
    """
    High level function for plotting the data returned from the Read function
    """
    viewer_fig = plt.figure()
    viewer_ax = viewer_fig.add_subplot(111)
    
    global x_label,y_label
    
    #Finding the column names
    columns = []
    for dd in data_dicts:
        data = dd["data"]
        for datatype_name in data.dtype.names:
            if(datatype_name not in columns): columns.append(datatype_name)
            
    x_label = columns[x_label] #default with 1st and 2nd column
    y_label = columns[y_label]
    
    #Draw viewer for the 1st time
    drawViewFigure(viewer_fig,data_dicts,x_label,y_label)
     
    #Creating the controls
    controls_fig = plt.figure()
    
    #Drawing the radio buttons that control the X and Y Axes
    radio_buttons = drawAxesControls(controls_fig,viewer_fig,columns)
    
    plt.show()

if __name__ == '__main__':
    if(len(sys.argv)>1):
        data_dicts = []
        for filename in sys.argv[1:]: data_dicts.append(Read(filename))
        
        Plot(data_dicts)
    
    else:
        print "usage: BlackBoxDataVisualiser [data file 1] [data file 2] ... [data file n]"