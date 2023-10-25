# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 09:45:15 2023

@author: cycon
"""
import sys
sys.path.append('/Lib/')
# import Lib.GasDynamics as GD
import numpy as np
import Lib.EngineErrors as EngineErrors

# Use to define the general states/functions shared by each/most stages
class Stage():
    def __init__(self, **kwargs):
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
        # General properties that could be used by all stages 
        # so all components know the atm conditions
        self.Ta  = kwargs.get('Ta') 
        self.Pa  = kwargs.get('Pa')
        self.Vinf = kwargs.get('Vinf')
        self.Minf = kwargs.get('Minf')
        
        self.Toi = kwargs.get('Toi')
        self.Poi = kwargs.get('Poi')
        self.Ti  = kwargs.get('Ti')
        self.Pi  = kwargs.get('Pi')
        self.Mi  = kwargs.get('Mi')
        self.Vi  = kwargs.get('Vi')
        
        self.m_dot = kwargs.get('m_dot') # Stays constant through component
        self.ni   = kwargs.get('ni', 1) # Isentropic efficiency
        
        self.Toe = kwargs.get('Toe')
        self.Poe = kwargs.get('Poe')
        self.Te  = kwargs.get('Te')
        self.Pe  = kwargs.get('Pe')
        self.Me  = kwargs.get('Me')
        self.Ve  = kwargs.get('Ve')
        
        self.StageName = ""
        self.Power = None
        
    def forward(self, next_Stage):
        next_Stage.Toi = self.Toe
        next_Stage.Poi = self.Poe
        next_Stage.Ti  = self.Te
        next_Stage.Pi  = self.Pe
        next_Stage.Mi  = self.Me
        next_Stage.Vi  = self.Ve
        next_Stage.m_dot = self.m_dot
    
    def printOutputs(self):
        form ='{:9.3f}'
        print('Stage: ', self.StageName)
        if self.Toe != None:
            print('\t Toe = {} K'.format(form).format(self.Toe))
        if self.Poe != None:
            print('\t Poe = {} '.format(form).format(self.Poe))
        if self.Te != None:
            print('\t Te  = {} K'.format(form).format(self.Te))
        if self.Pe != None:
            print('\t Pe  = {}'.format(form).format(self.Pe))
        print('\tmdot = {} kg/s'.format(form).format(self.m_dot))
        if self.Me != None:
            print('\t Me  = {}'.format(form).format(self.Me))
        if self.Ve != None:
            print('\t Ve  = {} m/s'.format(form).format(self.Ve))
        if self.Power != None:
            print('\t Pow = {} W'.format(form).format(self.Power))
        
        
class Intake(Stage):
    def __init__(self, **kwargs):
        Stage.__init__(self, **kwargs)
        self.StageName = "Intake"
        # NOTE: Ram efficiency ~= Isentropic Efficiency
        
    def calculate(self):
        # Always assume Pi/Pa and Ti/Ta are given (atmos conditions)
        self.Pi = self.Pa
        self.Ti = self.Ta
        self.Vi = self.Vinf
        self.Mi = self.Minf
        # If no vel or mach num inputted, assume stationary
        if self.Mi == None:
            if self.Vi == None:
                self.Mi = 0
            else:
                self.Mi = self.Vi/np.sqrt(self.gam_a*self.R*self.Ti)
        
        # Now we should have mach num no matter what
        # and the static props (atm props)
        self.Toe = self.Ti * (1 + (self.gam_a-1)*(self.Mi**2)/2)
        self.Poe = self.Pi * (1 + self.ni*(self.Mi**2)*(self.gam_a-1)/2)**(self.gam_a/(self.gam_a-1))
        
class Compressor(Stage):
    def __init__(self, **kwargs):
        Stage.__init__(self, **kwargs)
        self.StageName = "Compressor"
        # Adding PR and BPR
        self.r = kwargs.get('rc') # Pressure Ratio of stage
        self.BPR = kwargs.get('BPR', 1) # Bypass Ratio: total mass flow (air)/mass flow through core
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
        self.Power = self.m_dot*self.cp_a*(self.Toe-self.Toi)
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
        self.StageName = "Combustor"
        self.dTo = kwargs.get('dTb')
        self.dPo = kwargs.get('dPb_dec', 0) # the pressure loss within the compressor as a decimal (0.05 = 5% loss)
        self.f  = kwargs.get('f')
        self.Q  = kwargs.get('Q_fuel')
        self.nb = kwargs.get('nb', 1) # Combustor efficiency
        
    def calculate(self):
        # Assuming we have the Ti and Pi from compressor/prev stage
        # We need to have the exit 
        if self.Toe == None: 
            # No Turbine inlet temp given
            if self.dTo == None: 
                # No combustor increase temp given
                if self.f == None and self.Q == None:
                    # No air-fuel ratio given, cant calculate temps
                    raise EngineErrors.MissingValue('Toe, dTo, or f&Q','Combustor')
                else: 
                    # We have f and Q to calculate exit temp
                    f_ideal = self.f*self.nb # inputted f would be actual
                    self.Toe = (f_ideal*self.Q + self.cp_a*self.Toi)/(self.cpg(1+f_ideal))
            else:
                # We dont have exit temp, but do have temp increase
                self.Toe = self.Toi + self.dTo
         # else: Dont need to use since we have what we need
             # We have turbine inlet temp (Te)
             
        self.Poe = self.Poi*(1-self.dPo)
        self.dTo = self.Toe - self.Toi # will use later for f calcs
         

class Turbine(Stage):
    def __init__(self, Comp_to_power, **kwargs):
        Stage.__init__(self, **kwargs)
        self.StageName = "Turbine"
        self.np = kwargs.get('np') # Polytropic efficiency
        self.nm = kwargs.get('nm',1)
        self.Compressor = Comp_to_power
        # Will have inlet temp, compressor power
        self.r  = kwargs.get('rt') # Add for later, not used now
        # this will be for generators or when turbine pressure ratio is specified
        
    def calculate(self):
        self.Power = self.Compressor.Power/self.nm
        # Calculate exit temp
        self.Toe = self.Toi - self.Power/(self.m_dot*self.cp_g)
        
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
        self.Poe = self.Poi*(1- (self.Toi-self.Toe)/self.Toi )**(1/m_frac)
        
class Nozzle(Stage):
    def __init__(self, air_type='hot', **kwargs):
        Stage.__init__(self, **kwargs)
        self.StageName = "Nozzle"
        if air_type == 'hot':
            self.gam = self.gam_g
        else:
            self.gam = self.gam_a
        
    def calculate(self):
        # Check if choked
        Tc = self.Toi*(2/(self.gam_g+1))
        Pc = self.Poi*(1 - (1/self.ni)*(1-Tc/self.Toi))**(self.gam/(self.gam-1))
        
        P_rat = self.Poi/self.Pa
        P_crit = self.Poi/Pc
        if P_rat > P_crit:
            # Nozzle is choked
            self.Pe = Pc
        else:
            self.Pe = self.Pa
        # This equation remains the same
        self.Te = self.Toi*2/(self.gam+1)
        #self.Toi*(1 - self.ni)*(1 - (self.Pe/self.Poi)**((self.gam-1)/self.gam))
    
            
class Engine():
    def __init__(self):
        print(None)
        # Will use to define and connect all of the stages so the 
        # outlets of one stage is the inputs for the next stages
        
        
class Turbofan():
    def __init__(self, **kwargs):
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
        
        gen_kwargs = {
            'Ta': kwargs.get('Ta'),
            'Pa': kwargs.get('Pa'),
            'Vinf': kwargs.get('Vinf'),
            'Minf': kwargs.get('Minf')}
        # Efficiencies
        ni = kwargs.get('ni',1) # Inlet
        nj = kwargs.get('nj',1) # Nozzle
        nf = kwargs.get('nf',1) # Compressor - Isentropic
        nc = kwargs.get('nc',1) # Compressor - Isentropic
        nt = kwargs.get('nt',1) # Turbine - Isentropic
        nb = kwargs.get('nb',1) # Cobustor
        nm = kwargs.get('nm',1) # Mechanical
        npf = kwargs.get('npf') # Fan - Polytropic
        npc = kwargs.get('npc') # Compressor - Polytropic
        npt = kwargs.get('npt') # Turbine - Polytropic
        # Pressure Ratios/Relations
        dP_b = kwargs.get('dP_combustor') # Decimal pressure drop in combustor
        rfan = kwargs.get('rfan') # Fan PR
        rc   = kwargs.get('rc')   # Compressor PR
        BPR = kwargs.get('BPR',1) # Bypass Ratio
        # Turbine Inlet
        To_ti = kwargs.get('T_turb_in') # K - Turbine inlet temp
        # Air Mass flow
        mdot = kwargs.get('mdot_a') # kg/s
        
        
        self.inlet = Intake(**gen_kwargs,ni=ni,m_dot=mdot)
        self.fan = Compressor(**gen_kwargs, rc=rfan, BPR=BPR, np=npf, ni=nf)
        self.BP_nozzle = Nozzle('cold',**gen_kwargs, ni=nj)
        self.HP_comp = Compressor(**gen_kwargs, rc=rc, np=npc, ni=nc)
        self.combustor = Combustor(**gen_kwargs, Toe=To_ti, dPb_dec=dP_b, ni=nb)
        self.HP_turb = Turbine(self.HP_comp, **gen_kwargs, nm=nm, ni=nt, np=npt)
        self.LP_turb = Turbine(self.fan, **gen_kwargs, nm=nm, ni=nt, np=npt)
        self.nozzle = Nozzle(**gen_kwargs, ni=nj) # Nozzle/Exhaust?
        
        self.AllStages = [[self.inlet, None ],
                          [self.fan, None], 
                          [self.HP_comp,  self.BP_nozzle],
                          [self.combustor,None],
                          [self.HP_turb, None],
                          [self.LP_turb, None],
                          [self.nozzle, None]]
        
    def calculate(self):
        for i in range(0,len(self.AllStages)):
            # Calculate each row and print outputs
            self.AllStages[i][0].calculate()
            self.AllStages[i][0].printOutputs()
            if self.AllStages[i][1] != None:
                self.AllStages[i][1].calculate()
                self.AllStages[i][1].printOutputs()
                
            # Move forward
            if i != len(self.AllStages)-1: # It is not at the end, so forward
                if self.AllStages[i+1][1] != None: 
                    # Means that this stage delivers to two stages -> fan
                    self.AllStages[i,0].forward(self.allStages[i+1][0],self.allStages[i+1][1])
                else:
                    self.AllStages[i,0].forward(self.allStages[i+1][0])
                    
    