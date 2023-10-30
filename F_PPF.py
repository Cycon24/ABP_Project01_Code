"""
@Author: ZainHita
Filename: Performance Parameters Functions
"""

import numpy as np

class funcs():
    def __init__(self):
        self.cpg = 1.148e3
        self.cpa = 1.005e3
        self.Γg  = 1.333
        self.Γa  = 1.4
        self.h25 = 43100e3

    def fct_thrust_over_mdot(self, mcdot, mfdot, Va, V9, V19, mdot):
        F = mcdot * (V9 - Va) + mfdot * (V19 - Va) 
        return F/mdot

    def fct_f(self, T02, T03, T04, T05, nb):
        num = self.cpg*T03 - self.cpa*T02
        den = nb*(self.h25 - self.cpg*T03)
        return num/den
    
    def fct_SFC(self,): # Do we need this?
        ...

    def fct_mdot(self, P, T, A, M, sect): # P_stat, T_stat, Area, Mach number, hot/cold
        R = 287 # J/(kg.K)
        rho = P/(R*T)
        if sect == 'cold':
            Γ = self.Γa
        elif sect == 'hot':
            Γ = self.Γg
        V = M * np.sqrt(Γ*R*T)
        mdot = rho * V * A
        return mdot


    def fct_TSFC(self, mfdot, F):
        return mfdot/F

    # def fct_nT(self, mdot, Cj, Ca, f):
    #     num = (Cj**2 - Ca**2)/2
    #     den = f*self.h25
    #     return num/den
    
    def fct_nT(self, T0, Tt0, Tt2, Tt3):
        num = Tt2 * T0
        den = Tt3 * T0
        return (1 - num/den)
    
    # def fct_nP(self, Cj, Ca):
    #     num = 2
    #     den = 1 + Cj/Ca
    #     return num/den

    def fct_nP(self, m0dot, mcdot, mhdot, C0, C9, C19):
        num = C0 * (mcdot*(C19 - C0) + mhdot(C9 - C0))
        den = 0.5 * (mhdot*C9**2 + mcdot*C19**2 - m0dot)
        return num/den
        
    def fct_nO(self, nP, nT):
        return nP*nT
    

