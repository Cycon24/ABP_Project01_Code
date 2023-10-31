"""
@author: ZainHita
Filename: Sweep to Plot
"""
import BPR_Sweep as bpr
import fanPR_Sweep as fpr
import compPR_Sweep as cpr
from G_Plotter import graphs

# region BPR
draw = graphs('BPR')

draw.update(bpr.F_mdot_i,'F_over_mdot','ideal') # yvals, yname, choice
draw.update(bpr.TSFC_i,'TSFC','ideal') # yvals, yname, choice
draw.update(bpr.f_i,'f','ideal') # yvals, yname, choice
draw.update(bpr.nt_i,'nT','ideal') # yvals, yname, choice
draw.update(bpr.np_i,'nP','ideal') # yvals, yname, choice
draw.update(bpr.no_i,'nO','ideal') # yvals, yname, choice

draw.update(bpr.F_mdot_r,'F_over_mdot','real') # yvals, yname, choice
draw.update(bpr.TSFC_r,'TSFC','real') # yvals, yname, choice
draw.update(bpr.f_r,'f','real') # yvals, yname, choice
draw.update(bpr.nt_r,'nT','real') # yvals, yname, choice
draw.update(bpr.np_r,'nP','real') # yvals, yname, choice
draw.update(bpr.no_r,'nO','real') # yvals, yname, choice
# endregion

# region FPR
draw = graphs('FPR')

draw.update(fpr.F_mdot_i,'F_over_mdot','ideal') # yvals, yname, choice
draw.update(fpr.TSFC_i,'TSFC','ideal') # yvals, yname, choice
draw.update(fpr.f_i,'f','ideal') # yvals, yname, choice
draw.update(fpr.nt_i,'nT','ideal') # yvals, yname, choice
draw.update(fpr.np_i,'nP','ideal') # yvals, yname, choice
draw.update(fpr.no_i,'nO','ideal') # yvals, yname, choice

draw.update(fpr.F_mdot_r,'F_over_mdot','real') # yvals, yname, choice
draw.update(fpr.TSFC_r,'TSFC','real') # yvals, yname, choice
draw.update(fpr.f_r,'f','real') # yvals, yname, choice
draw.update(fpr.nt_r,'nT','real') # yvals, yname, choice
draw.update(fpr.np_r,'nP','real') # yvals, yname, choice
draw.update(fpr.no_r,'nO','real') # yvals, yname, choice
# endregion

# region CPR
draw = graphs('CPR')

draw.update(cpr.F_mdot_i,'F_over_mdot','ideal') # yvals, yname, choice
draw.update(cpr.TSFC_i,'TSFC','ideal') # yvals, yname, choice
draw.update(cpr.f_i,'f','ideal') # yvals, yname, choice
draw.update(cpr.nt_i,'nT','ideal') # yvals, yname, choice
draw.update(cpr.np_i,'nP','ideal') # yvals, yname, choice
draw.update(cpr.no_i,'nO','ideal') # yvals, yname, choice

draw.update(cpr.F_mdot_r,'F_over_mdot','real') # yvals, yname, choice
draw.update(cpr.TSFC_r,'TSFC','real') # yvals, yname, choice
draw.update(cpr.f_r,'f','real') # yvals, yname, choice
draw.update(cpr.nt_r,'nT','real') # yvals, yname, choice
draw.update(cpr.np_r,'nP','real') # yvals, yname, choice
draw.update(cpr.no_r,'nO','real') # yvals, yname, choice
# endregion