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

        screen_width = 1920
        screen_height = 1080

        width = screen_width / 150 # inches
        height = screen_height / 150 # inches

        # Number of subplots = num_of_rows*num_of_cols
        self.num_rows = 3    # Number of subplot rows
        self.num_cols = 2    # Number of subplot columns

        # Ideal case
        self.fig, self.axs = plt.subplots(self.num_rows, self.num_cols, sharex=True, figsize=(width, height))
          
        plotname = 'Performance Parameters vs ' + plotName + ' Variation'


        if plotName == 'BPR':
            self.xvals = np.linspace(5, 20, 100, endpoint = True)
            x_label = "Bypass Ratio"
        elif plotName == 'FPR':
            self.xvals = np.linspace(1.2, 2.0, 100, endpoint = True)
            x_label = r"$\pi_{fan}$"
        elif plotName == 'CPR':
            self.xvals = np.linspace(20, 40, 100, endpoint = True)
            x_label = r"$\pi_c$"
            
        self.labeller(self.axs, x_label, plotname)
        
    def labeller(self, mesh, plotName, plotNameVar):
        myPlot(mesh[0][0], ylabel="F/ṁ, (N/(kg/s))")
        myPlot(mesh[1][0], ylabel="TSFC, (g/(kN-s))")
        myPlot(mesh[2][0], xlabel=plotName, ylabel="f")
        myPlot(mesh[0][1], ylabel=r"$\eta_T$")
        myPlot(mesh[1][1], ylabel=r"$\eta_P$")
        myPlot(mesh[2][1], xlabel=plotName, ylabel=r"$\eta_O$")
        self.fig.suptitle(plotNameVar, fontsize=16)
        self.fig.legend(('Ideal','Real'))

    def update(self, yvalsi, yvalsr, yname): # yvals: numbers, yname = F_over_mdot/TSFC/f/nT/nP/nO, choice = real/ideal
        premesh = self.axs
       
        # Changed to 2d subplot matrix
        if yname == 'F_over_mdot':
            mesh = premesh[0][0]
        elif yname == 'TSFC':
            mesh = premesh[1][0]
        elif yname == 'f':
            mesh = premesh[2][0]
        elif yname == 'nT':
            mesh = premesh[0][1]
        elif yname ==  'nP':
            mesh = premesh[1][1]
        elif yname == 'nO':
            mesh = premesh[2][1]
        
        mesh.plot(self.xvals, yvalsi, 'b--', label="Ideal") 
        mesh.plot(self.xvals, yvalsr, 'k', label="Real")   
        if yname == 'F_over_mdot':
                handles, labels = mesh.get_legend_handles_labels()
                self.fig.legend(handles, labels, loc="upper center",bbox_to_anchor=(0.5,0.95),ncols=2)           
        
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
        self.colors = ['g', 'b', 'g', 'r', 'c', 'm', 'y']
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
        if self.legend != None:
            self.ax.legend()

        # Keeps track of initialization
        self.init = True   
    

