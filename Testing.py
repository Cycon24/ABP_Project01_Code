# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:23:02 2023

@author: cycon
"""

import EngineModule as EM

npc = 0.87 
npt = 0.87 
ni  = 0.95 
nj  = 0.95 
nm  = 0.99 
dP_b = 0.06 
nb  = 0.97 

Ta = 242.7 # K
Pa = 0.411 # bar
rc = 8.0 
Ttoi = 1200 # K - Turbine inlet temp

mdot = 15 # kg/s
Ci  = 260 # m/s

noz = EM.Intake(Ti=Ta, Pi=Pa, ni=ni,m_dot=mdot,Vi=Ci)
noz.calculate()
print(noz.Toe, noz.Poe)