# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 13:34:16 2023

@author: cycon
"""
from EngineModule import Turbofan_SingleSpool as Turbofan
# =============================================================================
#   Engine Input Parameters
# =============================================================================

turbofan_kwargs = {
    'Ta': 216.775, # Req
    'Pa': 22696.8, # Req
    'Vinf': None, # Or Minf
    'Minf': 0.85, # Or Vinf, if none its assumed stationary
    'ni': 0.98, # Inlet
    'nj': 0.99, # Nozzle
    'nf': None, # Compressor - Isentropic
    'nc': None, # Compressor - Isentropic
    'nt': None, # Turbine - Isentropic
    'nb': 0.99, # Cobustor
    'nm': 0.99, # Mechanical
    'npf': 0.89, # Fan - Polytropic
    'npc': 0.90, # Compressor - Polytropic
    'npt': 0.90, # Turbine - Polytropic
# Pressure Ratios/Relations
    'dP_combustor': 1-0.96, # Decimal pressure drop in combustor
    'rfan': 1.5, # Req - Fan PR
    'rc': 36,   # Req - Compressor PR
    'BPR': 10,     # Req Bypass Ratio
# Turbine Inlet
    'T_turb_in': 1560, # Req - K - Turbine inlet temp
# Air Mass flow
    'mdot_a': None,   # kg/s
# Fuel dH
    'Q_fuel': 43100 # kJ/kg
    }
# Print Inputs
print('Inputs')
for key,val in turbofan_kwargs.items():
    print('\t {}  =  {}'.format(key,val))
    
# =============================================================================
#     Calculation
# =============================================================================
Engine = Turbofan(**turbofan_kwargs)
# Force full expansion
Engine.BP_nozzle.Pe = turbofan_kwargs['Pa']
Engine.nozzle.Pe = turbofan_kwargs['Pa']
# Calculate 
Engine.calculate()