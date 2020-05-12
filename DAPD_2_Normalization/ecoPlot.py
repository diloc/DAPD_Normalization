# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 16:55:10 2020

@author: Diloz
"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.transforms as mtransforms


# def STD(feature, matrix, line, dayInt, dayFnl, EXP, pathSTD, flag):
def STD(pathSTD, EXP, line, feature, flag, matrix,  locat, dayInt, dayFnl):
    time = matrix['days']
    mean = matrix['mean'].values
    STD = matrix['STD'].values  
    daysI = np.arange(dayInt, dayFnl, 1)
    
    if feature == 'area': 
        units = ' [' + r'$mm^{2}$'+']'
        maxRV = 3000
        labelY = maxRV - 300
    
    if feature == 'leaf': 
        units = ' [Number]'
        maxRV = 40
        labelY = maxRV - 5
    
    fig, Adj = plt.subplots(1, 1, figsize=(12,12))

    for cntInt in daysI:
        if cntInt == np.min(daysI):
            Adj.fill_between((cntInt+(6/24), cntInt + (18/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1, label= 'Daytime')             
        else:
            Adj.fill_between((cntInt+(6/24), cntInt + (18/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1)

    dayUnits = 'Days [DAS]' 

    if flag == 'areaNormal': dayUnits = 'Days [DAPD]'

    Adj.plot(time, mean, color = 'b', label='Mean')    
    Adj.fill_between(time, mean - STD, mean + STD, color='blue', alpha=0.2, label = 'Standard Deviation')
    
     
    Adj.tick_params(direction='out', length=6, width=2, colors='black', labelsize = 24)
    Adj.set_xlabel(dayUnits, fontsize=24, fontdict=dict(weight='bold'))
    Adj.set_ylabel(feature + units, fontsize=24, fontdict=dict(weight='bold'))
    Adj.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    Adj.set_xlim([dayInt, dayFnl])
    Adj.set_ylim([0, maxRV])
    
    Adj.set_title(flag, fontsize=20)
    
    if line == 'Col0': line = 'Col-0'
    if line == 'col-0': line = 'Col-0'

    
    lineName= line[0].upper() + line[1:]
    Adj.text(daysI[0] + 2, labelY, lineName,fontsize=62, style='italic',
        bbox={'facecolor': 'white', 'pad': 10})


    filename = EXP + '_' +  line +  '_'  + feature + '_' + flag + '_'  + 'STD'

    fig.savefig(pathSTD + filename + '.' + 'png' , dpi= 300)

  
#%%   
def curves(pathCur, EXP, line, feature, flag, matrix,  locat, dayInt, dayFnl):  
    positions = locat.loc[:, 'posn']
    time = matrix['mins'] / (24*60)
    mean = matrix['mean'].values
    STD = matrix['STD'].values  
    daysI = np.arange(dayInt, dayFnl, 1)
    
    
    if feature == 'area': 
        units = ' [' + r'$mm^{2}$'+']'
        maxRV = 3000
        
    if feature == 'leaf': 
        units = ' [' + 'number' +']'
        maxRV = 40
    
    fig, Adj = plt.subplots(1, 1, figsize=(12,12))

    for cntInt in daysI:
        if cntInt == np.min(daysI):
            Adj.fill_between((cntInt+(7/24), cntInt + (21/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1)             
            # Adj.fill_between((cntInt+(7/24), cntInt + (21/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1, label= 'Daytime')             
        else:
            Adj.fill_between((cntInt+(7/24), cntInt + (21/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1)

    dayUnits = 'Days [DAPD]'
    
    if flag == 'normal': dayUnits = 'Days [DAPD]'

    for cntP in range(len(positions)):
        posn, cam = [], []
        posn = locat.loc[cntP, 'posn']
        cam = locat.loc[cntP, 'camera']
        fileOri =  matrix.loc[:, ['mins', posn]]
        fileOri.dropna(inplace=True)

        days = (fileOri.loc[:, 'mins'].values) / (24*60)
        areaP = fileOri.loc[:, posn].values

        if feature == 'leaf': 
            Adj.plot(days, areaP, '.', label=posn + ' ' + cam)
            labelY = maxRV - 5
            
        if feature == 'area':
            Adj.plot(days, areaP, label=posn + ' ' + cam)
            # Adj.legend(loc='upper left', shadow=True, fontsize= 24, edgecolor = 'Indigo')
            labelY = maxRV - 300
                
        Adj.tick_params(direction='out', length=6, width=2, colors='black', labelsize = 24)
        Adj.set_xlabel(dayUnits, fontsize=24, fontdict=dict(weight='bold'))
        Adj.set_ylabel(feature +  units, fontsize=24, fontdict=dict(weight='bold'))
        Adj.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
        Adj.set_xlim([dayInt, dayFnl])
        Adj.set_ylim([0, maxRV])

    lineName= line[0].upper() + line[1:]

    Adj.text(daysI[0] + 2, labelY, lineName,fontsize=62, style='italic',
        bbox={'facecolor': 'white', 'pad': 10})

    filename = EXP + '_' +  line +  '_'  + feature + '_' + flag + '_'  + 'curves' 
    fig.savefig(pathCur + filename + '.' + 'png' , dpi= 300)
        
        
    
def signif(feature, matrix, line, accRef, dayInt, dayFnl, EXP, pathSig, flag):
    time = matrix['mins'] / (24*60)
    meanRef = matrix['meanRef']
    meanTest = matrix['meanTest']
    
    STDRef = matrix['STDRef']
    STDTest = matrix['STDTest']
    
    

    daysI = np.arange(dayInt, dayFnl, 1)
    
    if feature == 'area': 
        units = ' [' + r'$mm^{2}$'+']'
        maxRV1 = np.ceil((np.max(meanRef + 1*STDRef)/500))* 500
        maxRV2 = np.ceil((np.max(meanTest + 1*STDTest)/500))* 500
        maxRV = np.maximum(maxRV1, maxRV2)
        maxRV = 3000
    
    if feature == 'leaf': 
        units = ' [Number]'
        maxRV1 = np.ceil((np.max(meanRef + 1*STDRef)/10))* 10
        maxRV2 = np.ceil((np.max(meanTest + 1*STDTest)/10))* 10
        maxRV = np.maximum(maxRV1, maxRV2)
        maxRV = 40
        # maxRV = np.ceil((np.max(mean + 1*STD)/10))* 10
    
    fig, Adj = plt.subplots(1, 1, figsize=(12,12))

    for cntInt in daysI:
        if cntInt == np.min(daysI):
            # Adj.fill_between((cntInt+(7/24), cntInt + (21/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1, label= 'Daytime')             
            Adj.fill_between((cntInt+(7/24), cntInt + (21/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1)             
        else:
            Adj.fill_between((cntInt+(7/24), cntInt + (21/24)), (0,0), (maxRV, maxRV),color='orange', alpha=0.1)
    
    
    meanRef = matrix['meanRef']
    meanTest = matrix['meanTest']
    
    STDRef = matrix['STDRef']
    STDTest = matrix['STDTest']

    alpha = 0.05
    
    markX, markY = [], []

    for cnt4 in range(len(time)):
        pvalue = matrix.loc[cnt4, 'pvalue']
        
        if pvalue <= alpha:
            markX.append(time[cnt4])
            markY.append(meanRef[cnt4])
    
    
    filename = EXP + '_' + flag + '_'  + 'Significant' + '_' +  line 
    filename = EXP + '_' +  line +  '_'  + 'Significant'+ '_' + flag   
    
    lineName= line[0].upper() + line[1:]

    refName = accRef[0].upper() + accRef[1:]
    
    if flag == 'raw': dayUnits = 'Days [DAS]' 
    if flag == 'normal': dayUnits = 'Days [DAPD]'
    if flag == 'normal_Original': dayUnits = 'Days [DAPD]'
    
    Adj.plot(time, meanRef, color = 'b', label='Col-0')
    Adj.plot(time, meanTest, color = 'g', label=lineName)
    Adj.scatter(markX, markY, c ="r", s=200, marker='X',label='p-value <= 0.05')
    Adj.errorbar(time, meanRef, STDRef, color = 'b', capsize=10, elinewidth=2, markeredgewidth=2, label='_nolegend_')
    Adj.errorbar(time, meanTest, STDTest, color = 'g', capsize=10, elinewidth=2, markeredgewidth=2, label='_nolegend_')
    
    Adj.tick_params(direction='out', length=6, width=2, colors='black', labelsize = 24)
    Adj.set_xlabel(dayUnits, fontsize=24, fontdict=dict(weight='bold'))
    Adj.set_ylabel(feature + units, fontsize=24, fontdict=dict(weight='bold'))
    Adj.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    Adj.set_xlim([dayInt, dayFnl])
    Adj.set_ylim([0, maxRV])
    Adj.legend(loc='upper left', shadow=True, fontsize= 24, edgecolor = 'Indigo')

    
    # Adj.set_title(line)
    fig.savefig(pathSig + filename + '.' + 'png' , dpi= 300)

    
       
        
        

    
    