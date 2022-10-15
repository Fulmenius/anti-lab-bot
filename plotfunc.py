# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 02:09:16 2020

@author: Fulmenius User
"""

import re
from inspect import signature
from readcol import read_col
import numpy as np
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp
import uncertainties as unc
import seaborn as sns
from scipy.optimize import curve_fit
from scipy import stats
import pandas as pd
from colorama import Fore, Back, Style
import math
from fnz_round import fnz_round

sns.set()

def plotfit(data, func, legend=True, torad=True):   #Takes the path to the data
    #torad - coversion of degs to radians, have no idea why it does not work properly without it
    #probably some issue with scipy.optimize
    #legend - turns legend on
    
    sign = signature(func) 
    sign = list(''.join(str(sign).split(', '))[1:-1]) #List of param names
    print(sign)
    x = np.array(read_col(0, data))*(1 + torad*(math.pi/180 - 1)) #Sample arguments 
    y = np.array(read_col(1, data)) #Sample values
    n = len(y) #number of entries in the sample
    
    popt, pcov = curve_fit(func, x, y) #Fitting data with a given func
    opts = popt
    
    print(Back.GREEN + 'Optimal values' + Style.RESET_ALL)
    for i in range(len(opts)):
        print(f"Optimal param {i}: {opts[i]}")
        
    optimal_params = opts
    
    r2 = 1.0-((sum((y - func(x, *opts)))**2)/((n-1.0)*np.var(y, ddof = 1))) #R squared
    print('R^2: ' + str(r2))
    
    uncts = unc.correlated_values(popt, pcov)
    print(Back.YELLOW + 'Uncertainty' + Style.RESET_ALL)
    for i in range(len(uncts)):
        print(f"Optimal param {i}: {uncts[i]}")
        
    labl = 'Params \n' + str([str(uncts[i]) for i in range(len(uncts))])    
        
    px = np.linspace(min(x) - 0.1*(max(x)-min(x)), max(x) +0.1*(max(x)-min(x)), 200)
    py = func(px, *optimal_params)
    
    nom = unp.nominal_values(py)
    std = unp.std_devs(py)
    
    def predband(x, xd, yd, p, func, conf = 0.95): #95% prediction interval
        alpha = 1.0 - conf
        N = xd.size
        var_n = len(p)
        q = stats.t.ppf(1.0 - alpha / 2.0, N - var_n)
        se = np.sqrt(1. / (N - var_n) * \
                 np.sum((yd - func(xd, *p)) ** 2))
    
        sx = (x - xd.mean()) ** 2
        sxd = np.sum((xd - xd.mean()) ** 2)
    
        yp = func(x, *p)
        dy = q * se * np.sqrt(1.0 + (1.0/ N) + (sx/sxd))
        lpb, upb = yp - dy, yp + dy
    
        return lpb, upb
    
    lpb, upb = predband(px, x, y, opts, func, conf = 0.95) #upper and lower boundary of the prediction interval
    
    print(labl)
    
    
    plt.plot(px, nom, c = 'black', label = labl)
    plt.plot(px, nom - 1.96 * std, c = 'orange', \
             label = '95% доверительный интервал')\
             
    plt.plot(px, nom + 1.96 * std, c = 'orange')
    
    plt.plot(px, lpb, 'k--', label = '95% предсказательный интервал')
    plt.plot(px, upb, 'k--')
    
    plt.scatter(x, y, s = 40, c = 'red', marker = '^', label = 'Экспериментальные данные')
    
    plt.ylabel('Ток, А')
    plt.xlabel('Угол, радианы')
    
    if legend:
        plt.legend(loc='best')
    
    plt.title("Зависимость интенсивности фототока от угла")
    plt.savefig('lab36graph1.png', dpi = 100) 
    plt.show()
    
    
    

        
    
    
    
    
        
    
    
plotfit('./laba46dat1', lambda x, a, b, c: a*(np.sin(b*x + c))**2)



 