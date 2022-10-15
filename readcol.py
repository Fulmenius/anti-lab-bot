# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 10:08:34 2020

@author: Fulmenius User
"""


def read_col(n, loc): #Чтение из файла n - ой колонки, колонки разделены проблелами или табами
    c = []
    file = open(loc, mode = 'r')
    for line in file:
        c.append((float(line.split()[n])))
        
    file.close()
    return c