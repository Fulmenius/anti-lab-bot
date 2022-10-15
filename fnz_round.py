# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 01:57:34 2020

@author: Fulmenius User

Округляет до n-ого знака после первого ненулевого
"""

import math

def fnz_round(x, n):
    return round(x, (x < 1)*-math.floor(math.log(x, 10))+n)

