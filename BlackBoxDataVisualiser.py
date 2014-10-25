#!/usr/bin/env python
import sys,copy
import numpy, matplotlib, matplotlib.pyplot as plt
from matplotlib.widgets import Slider,RadioButtons,CheckButtons

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
    title_row = 0
    
    #If header rows aren't specified, use the snooper helper function to try 
    if not(header_rows):
        header_rows = headerSnoop(raw_data,col_separator)
        title_row = header_rows-2
    
    title = raw_data[title_row].strip(col_separator)
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

def drawViewFigure(viewer_fig,data_dicts,x_label,y_label,parameter_selection,plot_type=matplotlib.lines.Line2D):
    """
    Helper function for drawing the view window for the x and y labels initially
    """
    #viewer_fig.clear()
    plt.figure(viewer_fig.number)
    viewer_ax = viewer_fig.add_subplot(111)
    
    for dd in data_dicts:
        title = dd["title"]
        data = numpy.copy(dd["data"])
        for parameter in parameter_selection.keys(): data = data[data[parameter]==parameter_selection[parameter]]
        
        if(x_label in data.dtype.names and y_label in data.dtype.names and plot_type==matplotlib.lines.Line2D): viewer_ax.plot(data[x_label],data[y_label],"-o",label=title)
        elif(x_label in data.dtype.names and y_label in data.dtype.names and plot_type==matplotlib.collections.PathCollection): viewer_ax.scatter(data[x_label],data[y_label],label=title)
        
    viewer_ax.set_xlabel(x_label)    
    viewer_ax.set_ylabel(y_label)
    
    viewer_fig.canvas.draw()
    plt.legend(loc='best')

def redrawViewFigure(viewer_fig,data_dicts,x_label,y_label,parameter_selection,plot_type=matplotlib.lines.Line2D):
    """
    Helper function for redrawing the view window for the x and y labels.
    """
    plt.figure(viewer_fig.number)
    viewer_ax = plt.gca()
    
    count = 0
    for vac in viewer_ax.get_children():
        if(isinstance(vac,plot_type)):
            title = data_dicts[count]["title"]
            data = numpy.copy(data_dicts[count]["data"])
            for parameter in parameter_selection.keys():
                #print parameter + " " + str(parameter_selection[parameter])
                data = data[data[parameter]==parameter_selection[parameter]]
            
            if(x_label in data.dtype.names and y_label in data.dtype.names and plot_type==matplotlib.lines.Line2D):
                vac.set_xdata(data[x_label])
                vac.set_ydata(data[y_label])
            elif(x_label in data.dtype.names and y_label in data.dtype.names and plot_type==matplotlib.collections.PathCollection): vac.set_offsets([data[x_label],data[y_label]])
                
            count += 1
        
    #for ax in viewer_fig.axes:
    viewer_ax.set_xlabel(x_label)    
    viewer_ax.set_ylabel(y_label)
    
    viewer_ax.relim() 
    viewer_ax.autoscale_view(True,True,True)
    
    viewer_fig.canvas.draw()
    
def drawAxesControls(controls_fig,viewer_fig,columns):
    """
    Helper function for adding the buttons for controlling the axes to the control view window
    """
    axcolor = 'w'
    char_width = max(map(lambda x:len(x),columns)) #finding the widest column title
    
                    #X offset, y offset, x length, y length
    rax = plt.axes([0.05, 0.1 + 0.03*len(columns) + 0.1, 0.015*char_width, 0.03*len(columns)], axisbg=axcolor,title="X Axis")  
    radio = RadioButtons(rax, tuple(columns))
    
    def x_axesChange(label):
        global x_label,y_label,parameter_selection,data_dicts #Should probably do this in a more OOP way
        x_label = label
        redrawViewFigure(viewer_fig,data_dicts,x_label,y_label,parameter_selection)
        
    radio.on_clicked(x_axesChange)
    
    rax2 = plt.axes([0.05, 0.1, 0.015*char_width, 0.03*len(columns)], axisbg=axcolor,title="Y Axis")
    radio2 = RadioButtons(rax2, tuple(columns))
    
    def y_axesChange(label):
        global x_label,y_label,parameter_selection,data_dicts
        y_label = label
        redrawViewFigure(viewer_fig,data_dicts,x_label,y_label,parameter_selection)
        
    radio2.on_clicked(y_axesChange)
    
    return [radio,radio2]

def drawParameterListControls(control_fig,viewer_fig,columns,default_values):
    """
    Helper function for adding the check boxes for controlling the parameter list
    """
    axcolor = 'w'
    char_width = max(map(lambda x:len(x),columns)) #finding the widest column title
    
    rax = plt.axes([0.05, 0.2 + 0.03*len(columns)*2 + 0.1, 0.015*char_width, 0.03*len(columns)], axisbg=axcolor,title="Parameter List")
    check = CheckButtons(rax, tuple(columns), ([True]*len(columns)))
    
    def parameterlistChange(label):
        global x_label,y_label,parameter_selection,data_dicts
        if(label in parameter_selection.keys()): del parameter_selection[label]
        else: parameter_selection[label] = default_values[columns.index(label)]
        
        redrawViewFigure(viewer_fig,data_dicts,x_label,y_label,parameter_selection)
    
    check.on_clicked(parameterlistChange)
    
    return check

def drawParameterControls(control_fig,viewer_fig,columns,default_values,min_values,max_values):
    """
    Helper function for adding the sliders for controlling the values of paramers
    """
    axcolor = 'w'
    char_width = max(map(lambda x:len(x),columns)) #finding the widest column title
    
    saxes = []
    sliders = {}
    
    #Generating the Sliders
    for i,c in enumerate(columns):
        saxes.append(plt.axes([0.05 + 0.015*char_width + 0.01*char_width + 0.05, (0.01 + 0.03)*i + 0.1, 0.02*char_width, 0.03], axisbg=axcolor))
        sliders[c] = Slider(saxes[-1], c, min_values[i], max_values[i], valinit=default_values[i])
        
    #The callback function for the sliders
    def parameterChange(value,column):
        global x_label,y_label,parameter_selection,data_dicts
    
        changed = False
        if(column in parameter_selection.keys()):
            if(parameter_selection[column]!=value):
                for dd in data_dicts:
                    nearest_value = dd["data"][column][numpy.argmin(numpy.abs(dd["data"][column]-value))]
                    parameter_selection[column] = nearest_value
                    sliders[column].set_val(nearest_value)
                    changed = True
        
        if(changed): redrawViewFigure(viewer_fig,data_dicts,x_label,y_label,parameter_selection)
       
    #Creating and bind a unique function call for each slider
    functions = []
    for column in columns:
        functions.append(lambda value,col=column: parameterChange(value,col))
        sliders[column].on_changed(functions[-1])

    return sliders

#Global variables used during plotting
x_label = 0
y_label = 1
parameter_selection = {}
data_dicts = []
    
def Plot(dd):
    """
    High level function for plotting the data returned from the Read function
    """
    viewer_fig = plt.figure()
    
    global x_label,y_label,parameter_selection,data_dicts
    data_dicts = dd
    
    #Finding the column names
    columns = []
    default_values = []
    min_values = []
    max_values = []
    for dd in data_dicts:
        data = dd["data"]
        for datatype_name in data.dtype.names:
            if(datatype_name not in columns):
                columns.append(datatype_name)
                default_values.append(data[datatype_name][0])
                min_values.append(min(data[datatype_name]))
                max_values.append(max(data[datatype_name]))
            
    #Setting Default Values
    x_label = columns[x_label]
    y_label = columns[y_label]
    
    #Adding the other parameter types to the dictionary
    for c in columns:
        if(c is not x_label or c is not y_label): parameter_selection[c] = default_values[columns.index(c)]
    
    plot_type = matplotlib.collections.PathCollection
    
    #Draw viewer for the 1st time
    drawViewFigure(viewer_fig,data_dicts,x_label,y_label,parameter_selection)
     
    #Creating the controls
    controls_fig = plt.figure()
    
    #Drawing the radio buttons that control the X and Y Axes
    axes_radio_buttons = drawAxesControls(controls_fig,viewer_fig,columns)
    parameter_list_checkboxes = drawParameterListControls(controls_fig,viewer_fig,columns,default_values)
    parameter_sliders = drawParameterControls(controls_fig,viewer_fig,columns,default_values,min_values,max_values)
    
    plt.show()

if __name__ == '__main__':
    if(len(sys.argv)>1):
        data_dicts = []
        for filename in sys.argv[1:]: data_dicts.append(Read(filename))
        
        Plot(data_dicts)
    
    else:
        print "usage: BlackBoxDataVisualiser [data file 1] [data file 2] ... [data file n]"