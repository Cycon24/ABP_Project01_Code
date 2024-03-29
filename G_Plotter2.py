"""
@author: ZainHita
Filename: Graphical Plotter
"""
import matplotlib.pyplot as plt 
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D
# from screeninfo import get_monitors
import numpy as np

plt.ion()  # enable interactive drawing

class graphs():
    def __init__(self, plotName): # Receives Plot Variable Parameter (BPR/FPR/CPR)

        # Determining Figure Size
        # monitors = get_monitors()
        # if monitors:
        #     screen_width = monitors[0].width
        #     screen_height = monitors[0].height
        # else:
            # Default Values if no monitor information is available
        screen_width = 1920
        screen_height = 1080

        width = screen_width / 200 # inches
        height = screen_height / 200 # inches

        # Number of subplots = num_of_rows*num_of_cols
        self.num_rows = 6    # Number of subplot rows
        self.num_cols = 1    # Number of subplot columns

        # Ideal case
        self.fig, self.ax = plt.subplots(self.num_rows, self.num_cols, sharex=True, figsize=(width, height))
        
        plotname = 'Ideal & Real Case with Variating ' + plotName + ' Data'

        self.labeller(self.ax, plotName, plotname)

        if plotName == 'BPR':
            self.xvals = np.linspace(5, 20, 100, endpoint = True)
        elif plotName == 'FPR':
            self.xvals == np.linspace(1.2, 2.0, 100, endpoint = True)
        elif plotName == 'CPR':
            self.xvals = np.linspace(20, 40, 100, endpoint = True)

    def labeller(self, mesh, plotName, plotNameVar):
        myPlot(mesh[0], ylabel='F/ṁ, (N/(kg/s))', title=plotNameVar)
        myPlot(mesh[1], ylabel='TSFC, (g/(kN-s))')
        myPlot(mesh[2], ylabel='f')
        myPlot(mesh[3], ylabel='η_T')
        myPlot(mesh[4], ylabel='η_P')
        myPlot(mesh[5], xlabel=plotName, ylabel='η_O')

    def update(self, yvalsi, yvalsr, yname): # yvals: numbers, yname = F_over_mdot/TSFC/f/nT/nP/nO, choice = real/ideal

        premesh = self.ax

        if yname == 'F_over_mdot':
            mesh = premesh[0]
        elif yname == 'TSFC':
            mesh = premesh[1]
        elif yname == 'f':
            mesh = premesh[2]
        elif yname == 'nT':
            mesh = premesh[3]
        elif yname == 'nP':
            mesh = premesh[4]
        elif yname == 'nO':
            mesh = premesh[5]

        mesh.plot(self.xvals, yvalsi, 'g', self.ax.vals, yvalsr, 'k')                    

class myPlot:
    ''' 
        Create each individual subplot.
    '''
    def __init__(self, ax,
                 xlabel='',
                 ylabel='',
                 title='',
                 legend=None):
        ''' 
            ax - This is a handle to the  axes of the figure
            xlable - Label of the x-axis
            ylable - Label of the y-axis
            title - Plot title
            legend - A tuple of strings that identify the data. 
                     EX: ("data1","data2", ... , "dataN")
        '''
        self.legend = legend
        self.ax = ax                  # Axes handle
        self.colors = ['g', 'b', 'k', 'r', 'c', 'm', 'y']
        # A list of colors. The first color in the list corresponds
        # to the first line object, etc.
        # 'b' - blue, 'g' - green, 'r' - red, 'c' - cyan, 'm' - magenta
        # 'y' - yellow, 'k' - black
        self.line_styles = ['-', '-', '-', '--', '-.', ':', ':-']
        # A list of line styles.  The first line style in the list
        # corresponds to the first line object.
        # '-' solid, '--' dashed, '-.' dash_dot, ':' dotted

        self.line = []

        # Configure the axes
        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel(xlabel)
        self.ax.set_title(title)
        self.ax.grid(True)

        # Keeps track of initialization
        self.init = True   
    

