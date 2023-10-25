# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 09:45:15 2023

@author: cycon
"""
import GasDynamics as GD
import numpy as np
import EngineErrors

# Use to define the general states/functions shared by each/most stages
class Stage():
    def __init_(self, **kwargs):
        '''

        Parameters
        ----------
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.R = 287 # J/kg*K
        self.gam_a = 1.4
        self.gam_g = 4/3
        self.cp_a = 1.005 # kJ/kg*K
        self.cp_g = 1.148 # kJ/kg*K
        # General properties that could be used by all
        # stages 
        self.Toi = kwargs.get('Toi')
        self.Poi = kwargs.get('Poi')
        self.Ti  = kwargs.get('Ti')
        self.Pi  = kwargs.get('Pi')
        self.Mi  = kwargs.get('Mi')
        self.Vi  = kwargs.get('Vi')
        
        self.m_dot = kwargs.get('m_dot') # Stays constant through component
        self.ni   = kwargs.get('ni', default=1) # Isentropic efficiency
        
        self.Toe = kwargs.get('Toe')
        self.Poe = kwargs.get('Poe')
        self.Te  = kwargs.get('Te')
        self.Pe  = kwargs.get('Pe')
        self.Me  = kwargs.get('Me')
        self.Ve  = kwargs.get('Ve')
        
    def forward(self, next_Stage):
        next_Stage.Toi = self.Toe
        next_Stage.Poi = self.Poe
        next_Stage.Ti  = self.Te
        next_Stage.Pi  = self.Pe
        next_Stage.Mi  = self.Me
        next_Stage.Vi  = self.Ve
        next_Stage.m_dot = self.m_dot
        
        
        
class Intake(Stage):
    def __init_(self, **kwargs):
        Stage.__init__(self, **kwargs)
        # NOTE: Ram efficiency ~= Isentropic Efficiency
        
    def calculate(self):
        # Always assume Pi and Ti are given (atmos conditions)
        # If no vel or mach num inputted, assume stationary
        if self.Mi == None:
            if self.Vi == None:
                self.Mi = 0
            else:
                self.Mi = self.Vi/np.sqrt(self.gam_a*self.R*self.Ti)
        
        # Now we should have mach num no matter what
        # and the static props (atm props)
        self.Toe = self.Ti * GD.To_T_ratio(self.Mi, self.gam_a)
        self.Poe = self.Pi * (1 + self.ni*(self.Mi**2)*(self.gam_a-1)/2)**(self.gam_a/(self.gam_a-1))
        
class Compressor(Stage):
    def __init_(self, **kwargs):
        Stage.__init__(self, **kwargs)
        # Adding PR and BPR
        self.r = kwargs.get('rc') # Pressure Ratio of stage
        self.BPR = kwargs.get('BPR', default=1) # Bypass Ratio: total mass flow (air)/mass flow through core
        self.np = kwargs.get('np') # Polytropic efficiency
        
    def calculate(self):
        # Should always have input To and Po, need to calculate power
        # and output To and Po. r will always be given, BPR will affect output 
        # to next stage
        if self.r == None:
            raise EngineErrors.MissingValue('R-Press. Ratio','Compressor')
        elif self.np == None:
            self.np = ((self.gam_a-1)/self.gam_a)*np.log(self.r) / \
                        np.log( (self.r**((self.gam_a-1)/self.gam_a) - 1)/self.ni + 1)
        
        n_frac =  (self.gam_a-1)/(self.gam_a*self.np)
        self.Toe = self.Toi + self.Toi*(self.r**n_frac - 1)
        self.Poe = self.r*self.Poi
        self.Power = self.m_dot*self.cp_a*(self.Te-self.Ti)
        # Done
        
    
    def forward(self, next_Stage_hot, next_Stage_cold=None):
        next_Stage_hot.Toi = self.Toe
        next_Stage_hot.Poi = self.Poe
        next_Stage_hot.Ti  = self.Te
        next_Stage_hot.Pi  = self.Pe
        next_Stage_hot.Mi  = self.Me
        next_Stage_hot.Vi  = self.Ve
        
        if next_Stage_cold == None:
            next_Stage_hot.m_dot = self.m_dot
        else:
            if self.BPR == None:
                raise EngineErrors.MissingValue('BPR','Compressor')
            else:
                m_dot_h = self.m_dot/self.BPR
                m_dot_c = self.m_dot - m_dot_h
                
                next_Stage_hot.m_dot = m_dot_h
                
                next_Stage_cold.Toi = self.Toe
                next_Stage_cold.Poi = self.Poe
                next_Stage_cold.Ti  = self.Te
                next_Stage_cold.Pi  = self.Pe
                next_Stage_cold.Mi  = self.Me
                next_Stage_cold.Vi  = self.Ve
                next_Stage_cold.m_dot = m_dot_c
                
        
        
    def calculate_nc(self, np, gamma=1.4):
        '''

        Parameters
        ----------
        np : Float, 0-1
            Polytropic efficiency.
        gamma : Float, optional
            Gamma. The default is 1.4.

        Returns
        -------
        Isentropic Efficiency.

        '''
        nc = ( self.r**((self.gam_a-1)/self.gam_a) - 1 ) / ( self.r**((self.gam_a-1)/(self.gam_a*np)) - 1 )
        return nc
        
        
class Combustor(Stage):
    def __init__(self, **kwargs):
        Stage.__init__(self, **kwargs)
        self.dT = kwargs.get('dTb')
        self.dP = kwargs.get('dPb_dec', 0) # the pressure loss within the compressor as a decimal (0.05 = 5% loss)
        self.f  = kwargs.get('f')
        self.Q  = kwargs.get('Q_fuel')
        self.nb = kwargs.get('nb', 1) # Combustor efficiency
        
    def calculate(self):
        # Assuming we have the Ti and Pi from compressor/prev stage
        # We need to have the exit 
        if self.Te == None: 
            # No Turbine inlet temp given
            if self.dT == None: 
                # No combustor increase temp given
                if self.f == None and self.Q == None:
                    # No air-fuel ratio given, cant calculate temps
                    raise EngineErrors.MissingValue('Te, dT, or f&Q','Combustor')
                else: 
                    # We have f and Q to calculate exit temp
                    f_ideal = self.f*self.nb # inputted f would be actual
                    self.Te = (f_ideal*self.Q + self.cp_a*self.Ti)/(self.cpg(1+f_ideal))
            else:
                # We dont have exit temp, but do have temp increase
                self.Te = self.Ti + self.dT
         # else: Dont need to use since we have what we need
             # We have turbine inlet temp (Te)
             
        self.Pe = self.Pi(1-self.dP)
        self.dT = self.Te - self.Ti # will use later for f calcs
         

class Turbine(Stage):
    def __init_(self, Comp_to_power, **kwargs):
        Stage.__init__(self, **kwargs)
        self.np = self.kwargs('np') # Polytropic efficiency
        self.nm = self.kwargs('nm',1)
        self.Pc = Comp_to_power.Power # The power USAGE of compressor
        # Will have inlet temp, compressor power
        self.r  = self.kwargs('rt') # Add for later, not used now
        # this will be for generators or when turbine pressure ratio is specified
        
    def calculate(self):
        self.Power = self.Pc/self.nm
        # Calculate exit temp
        self.Te = self.Ti - self.Power/(self.m_dot*self.cp_g)
        
        if self.np == None:
            if self.r != None:
                # Calculate np
                self.np = np.log(1- self.ni*(1 - self.r**((self.gam_g-1)/self.gam_g)))
                self.np /= np.log(self.r)*(self.gam_g-1)/self.gam_g
            else:
                print('Warning: insufficient parameters given to turbine')
                print('Continuing assuming polytropic efficiency = 1')
                self.np = 1
                
        m_frac = self.np*(self.gam_g-1)/self.gam_g
        self.Pe = self.Pi*(1- (self.Ti-self.Te)/self.Ti )**(1/m_frac)
        
class Nozzle(Stage):
    def __init_(self, **kwargs):
        Stage.__init__(self, **kwargs)
        # Hello
        print(None)
    
class Engine():
    def __init__(self):
        print(None)
        # Will use to define and connect all of the stages so the 
        # outlets of one stage is the inputs for the next stages
        
        
class Turbofan(Engine):
    def __init__(self):
        # Stages
        # Atm moving
        # Inlet
        # Fan  (is a compressor)
        # Bypass Nzzle
        # LP Compressor
        # HP Compressor
        # Combustor
        # HP Turbine
        # LP Turbine
        # Nozzle
        self.inlet = Intake()
        self.fan = Compressor()
        self.BP_nozzle = Nozzle()
        # self.LP_comp = Compressor()
        self.HP_comp = Compressor()
        self.combustor = Combustor()
        self.HP_turb = Turbine(self.HP_comp)
        self.LP_turb = Turbine(self.fan)
        self.nozzle = Nozzle() # Nozzle/Exhaust?
        
        self.AllStages = [self.inlet, self.fan, self.BP_nozzle, self.LP_comp, self.HP_comp, self.combustor, self.HP_turb, self.LP_turb, self.nozzle]
        
    