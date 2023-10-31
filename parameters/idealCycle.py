# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 20:08:40 2023

@author: cycon
"""

turbofan_kwargs = {
    'Ta': 216.775, # Req - Pulled from hand calculations
    'Pa': 22696.8, # Req
    'Vinf': None, # Or Minf
    'Minf': 0.85, # Or Vinf, if none its assumed stationary
    'ni': 1, # Inlet
    'nj': 1, # Nozzle
    'nf': None, # Compressor - Isentropic
    'nc': None, # Compressor - Isentropic
    'nt': None, # Turbine - Isentropic
    'nb': 1, # Cobustor
    'nm': 1, # Mechanical
    'npf': 1, # Fan - Polytropic
    'npc': 1, # Compressor - Polytropic
    'npt': 1, # Turbine - Polytropic
    'dP_combustor': 0, # Decimal pressure drop in combustor
    'rfan': 1.5, # Req - Fan PR
    'rc': 36,   # Req - Compressor PR
    'BPR': 10,     # Req Bypass Ratio
    'T_turb_in': 1560, # Req - K - Turbine inlet temp
    'mdot_a': None,   # kg/s
    }