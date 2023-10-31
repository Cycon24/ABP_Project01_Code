# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 20:08:05 2023

@author: cycon
"""

turbofan_kwargs = {
    'Ta': 216.775, # Req - Pulled from hand calculations
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
    'dP_combustor': 1-0.96, # Decimal pressure drop in combustor
    'rfan': 1.5, # Req - Fan PR
    'rc': 36,   # Req - Compressor PR
    'BPR': 10,     # Req Bypass Ratio
    'T_turb_in': 1560, # Req - K - Turbine inlet temp
    'mdot_a': None,   # kg/s
    'Q_fuel': 43100 # kJ/kg
    }