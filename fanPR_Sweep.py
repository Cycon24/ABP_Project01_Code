# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 23:11:34 2023

@author: cycon
"""
from EngineModule import Turbofan_SingleSpool as Turbofan
from F_PPF import funcs 
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/parameters/')
import parameters.realCycle as RC 
import parameters.idealCycle as IC 

ideal_kwargs = IC.turbofan_kwargs.copy()
real_kwargs = RC.turbofan_kwargs.copy()
functions = funcs()

# Define BPR range
fan_PRs = np.linspace(1.2,2,100, endpoint=True)

# Inittialize perf param arrays
F_mdot_r = []
TSFC_r = []
f_r = []
nt_r = []
np_r = []
no_r = []

F_mdot_i = []
TSFC_i = []
f_i = []
nt_i = []
np_i = []
no_i = []

# Thrust from hand calcs
F = 70209.67 # N

for fPR in fan_PRs:
    # Set BPR to current BPR to calculate
    ideal_kwargs['rfan'] = fPR
    real_kwargs['rfan'] = fPR
    # Setting this here so I dont have to rewrite some equations
    bpr = ideal_kwargs['BPR']
    
    # Initialize turbofans
    real_tf = Turbofan(**real_kwargs)
    ideal_tf = Turbofan(**ideal_kwargs)
    
    # Force full expansion
    real_tf.BP_nozzle.Pe = real_kwargs['Pa']
    real_tf.nozzle.Pe = real_kwargs['Pa']
    ideal_tf.BP_nozzle.Pe = ideal_kwargs['Pa']
    ideal_tf.nozzle.Pe = ideal_kwargs['Pa']
    
    # Analyze engines
    # print('Real')
    # real_tf.printInputs()
    real_tf.calculate(False)
    # print('Ideal')
    # ideal_tf.printInputs()
    ideal_tf.calculate(False)
    
    # Get outputs
    real_outs = real_tf.getOutputs() # Note: f in real case is calculated, but not in ideal
    ideal_outs = ideal_tf.getOutputs()
    
    # Calculate overall airflow NOTE: Ignoring fuel flow in ideal case
    mdot_r = functions.fct_mdot2(F, bpr, real_outs['C9'],real_outs['C19'],real_outs['Ca'], real_outs['f'])
    mdot_i = functions.fct_mdot2(F, bpr, ideal_outs['C9'],ideal_outs['C19'],ideal_outs['Ca'])
    # Calculate core and bypass flow
    mdot_h_r = mdot_r/(1 + bpr)      # Hot real (core-without fuel)
    mdot_c_r = mdot_r - mdot_h_r     # Cold real (bypass)
    mdot_f_r = mdot_h_r*real_outs['f'] # Fuel flow kg/s
    mdot_g_r = mdot_h_r + mdot_f_r   # Core Exhuast real (with fuel)
    
    mdot_h_i = mdot_i/(1 + bpr)     # Hot ideal (core)
    mdot_c_i = mdot_i - mdot_h_i     # Cold ideal (bypass)
    f_i.append(functions.fct_f(ideal_outs['To3'],ideal_outs['To4'],ideal_outs['nb']))
    mdot_f_i = mdot_h_i*f_i[-1] # Fuel flow kg/s
    
    # Calculate the needed perf params:
    F_mdot_r.append(F/mdot_r)
    F_mdot_i.append(F/mdot_i)
    
    f_r.append(real_outs['f'])
    # f_i already appended above
    
    # Equations specifc for turbofans - from Prof
    TSFC_r.append(f_r[-1]*3600/((1+bpr)*F/mdot_r))
    TSFC_i.append(f_i[-1]*3600/((1+bpr)*F/mdot_i))
    
    nt_r.append(functions.fct_nT(mdot_r, mdot_h_r, mdot_c_r, mdot_f_r, real_outs['C9'],real_outs['C19'],real_outs['Ca']))
    nt_i.append(functions.fct_nT(mdot_i, mdot_h_i, mdot_c_i, mdot_f_i, ideal_outs['C9'],ideal_outs['C19'],ideal_outs['Ca']))
    
    np_r.append(functions.fct_nP(mdot_r, mdot_c_r, mdot_h_r, real_outs['Ca'], real_outs['C9'],real_outs['C19']))
    np_i.append(functions.fct_nP(mdot_i, mdot_c_i, mdot_h_i, ideal_outs['Ca'], ideal_outs['C9'],ideal_outs['C19']))
    
    no_r.append(np_r[-1]*nt_r[-1])
    no_i.append(np_i[-1]*nt_i[-1])
    


