# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 21:58:28 2018

@author: dlozano
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def  CVS(pathCSV, fName, df):   
    # pathCSV = root+EXP + '_' + folder +'/'
    if not os.path.exists(pathCSV):
        os.makedirs(pathCSV)
    df.to_csv (pathCSV + fName+ '.csv' , index = None, header=True)
    # df.to_csv (pathCSV + '.csv' , index = None, header=True)

def plot(root,EXP,folder,fName, fType, fig, extension, quality):
    pathPLOT = root+EXP + '_' + folder +'/'+fType +'/'
    if not os.path.exists(pathPLOT):
        os.makedirs(pathPLOT)
    fig.savefig(pathPLOT + fName +'_'+fType + '.' + extension , dpi= quality)