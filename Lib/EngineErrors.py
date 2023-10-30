# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:19:25 2023

@author: cycon
"""

class MissingValue(Exception):
    'Further computations cannot be completed due to missing values'
    def __init__(self, missing_prop_str, component_str):
        self.message = 'Missing Value: {} within {} component'.format(missing_prop_str, component_str)
        super().__init__(self.message)