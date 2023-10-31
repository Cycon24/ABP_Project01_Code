"""
@author: ZainHita
Filename: Sweep to Plot
"""
import BPR_Sweep as bpr
import fanPR_Sweep as fpr
import compPR_Sweep as cpr
from G_Plotter import graphs
import matplotlib.pyplot as plt
plt.close('all')
# region BPR
draw = graphs('BPR')

draw.update(bpr.F_mdot_i,bpr.F_mdot_r,'F_over_mdot',) # yvals, yname, choice
draw.update(bpr.TSFC_i,bpr.TSFC_r,'TSFC') # yvals, yname, choice
draw.update(bpr.f_i,bpr.f_r,'f') # yvals, yname, choice
draw.update(bpr.nt_i,bpr.nt_r,'nT') # yvals, yname, choice
draw.update(bpr.np_i,bpr.np_r,'nP') # yvals, yname, choice
draw.update(bpr.no_i,bpr.no_r,'nO') # yvals, yname, choice

# endregion

# region FPR
draw = graphs('FPR')

draw.update(fpr.F_mdot_i,fpr.F_mdot_r, 'F_over_mdot') # yvals, yname, choice
draw.update(fpr.TSFC_i,fpr.TSFC_r,'TSFC') # yvals, yname, choice
draw.update(fpr.f_i,fpr.f_r,'f') # yvals, yname, choice
draw.update(fpr.nt_i,fpr.nt_r,'nT') # yvals, yname, choice
draw.update(fpr.np_i,fpr.np_r,'nP') # yvals, yname, choice
draw.update(fpr.no_i,fpr.no_r,'nO') # yvals, yname, choice
# endregion

# region CPR
draw = graphs('CPR')

draw.update(cpr.F_mdot_i,cpr.F_mdot_r, 'F_over_mdot') # yvals, yname, choice
draw.update(cpr.TSFC_i,cpr.TSFC_r,'TSFC') # yvals, yname, choice
draw.update(cpr.f_i,cpr.f_r,'f') # yvals, yname, choice
draw.update(cpr.nt_i,cpr.nt_r,'nT') # yvals, yname, choice
draw.update(cpr.np_i,cpr.np_r,'nP') # yvals, yname, choice
draw.update(cpr.no_i,cpr.no_r,'nO') # yvals, yname, choice

# endregion