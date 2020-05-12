# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 11:01:34 2020

@author: Diloz
"""

import pandas as pd
import numpy as np
import datetime
import data
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib.pylab as plt
from scipy import interpolate
import sys

#%%
def stoll(t,a,b):
    return (a* np.exp(t*b))
#%%
def detectDuplicate(feature, table, dayStart, dayStop, krnl):
    minStar = dayStart * (24*60)
    minStop = dayStop * (24*60)
    mtrx =  pd.DataFrame(columns=['index', 'daySpan', 'dayUnique'])
    table['total_measurements'] = ''
    table['fitError'] = ''
    table['duplicate'] = 'yes'
    
    posns = pd.unique(table['posn'])
    for posn in posns:
        idx = []
        idx = np.where(table['posn'] == posn)[0]

        for cnt in range(len(idx)):           
            nameFile, file = [], []
            mins, trait = [], []
            dayAll, dayAux, daySpn, dayUnq = [], [], [], []
            
            nameFile = table.loc[idx[cnt], 'folder'] + table.loc[idx[cnt], 'file'] 
            fileOri = pd.read_csv(nameFile)[['mins', feature]]
            fileAux = fileOri[(fileOri['mins']>= minStar) & (fileOri['mins']<= minStop)]
    
            mins = fileAux['mins'].values
            trait = fileAux[feature].values
            dayAll = (mins / (24*60))
            daySpn = len(dayAll)
            dayUnq = len(np.unique(np.int32(dayAll)))
            
            table['total_measurements'][idx[cnt]] = daySpn

            mtrx.loc[cnt, 'index'] = idx[cnt]
            mtrx.loc[cnt, 'daySpan'] = daySpn
            mtrx.loc[cnt, 'dayUnique'] = dayUnq
            
            
            if daySpn < krnl:
                table['fitError'][idx[cnt]] = np.inf
                mtrx.loc[cnt, 'fitError'] = np.inf
                continue
        
            intCond = [1e-5, 1e-5]
            [aStolMed, bStolMed], pcov = curve_fit(stoll, mins, trait, intCond)
            perr = np.linalg.norm(np.sqrt(np.diag(pcov)))
            
            table['fitError'][idx[cnt]] = perr
            mtrx.loc[cnt, 'fitError'] = perr
        
        mtrx.sort_values(by = ['dayUnique', 'fitError', 'daySpan'],ascending=[False, True, False],  inplace=True)
        mtrx.reset_index(drop=True, inplace=True) 
        idx3 = []
        idx3 = mtrx.loc[0, 'index']
        table['duplicate'][idx3] = 'no'
        
    return table

#%% Read the original CSV files and generate a time matrix, trait matrix and time vector
def seriesSize(feat1, feat2, ecos, krnl, dateST, dayInt, dayFnl):
    locat  = pd.DataFrame([])
    minsFAll = pd.DataFrame([])
    trait1FAll, trait2FAll = pd.DataFrame([]), pd.DataFrame([])
    posns, cams, minsVec = [], [], []
    minStar = dayInt * (24*60)
    minStop = dayFnl * (24*60)

    for cnt3 in range(len(ecos)):
        nameFile, fileOri, fileAux = [], [], []
        mins, minsF = [], []
        trait1, trait2, trait1F, trait2F  = [], [], [], []
        posn, cam = [], []
        posn = ecos.posn[cnt3]
        cam = ecos.camera[cnt3]
        nameFile = ecos.folder[cnt3] + ecos.file[cnt3]
        fileOri = pd.read_csv(nameFile)[['mins', feat1, feat2]]
        fileAux = fileOri[(fileOri['mins']>= minStar) & (fileOri['mins']<= minStop)]
        fileAux = fileAux.drop_duplicates(subset ='mins') 
        fileAux.drop(fileAux[fileAux['mins'] < 10 ].index , inplace=True) # Remove very short time-reies
        fileAux.drop(fileAux[fileAux[feat1] > 4000 ].index , inplace=True) # Remove very short time-reies
        fileAux.drop(fileAux[fileAux[feat1] < 10 ].index , inplace=True) # Remove very short time-reies
        mins = fileAux['mins'].values
        trait1 = fileAux[feat1].values
        trait2 = fileAux[feat2].values
        
        if len(mins) < krnl: continue
    
        mins = timeAdjust(mins, dayInt, dayFnl, 5)
        minsF, trait1F, trait2F = mins, trait1, trait2
        posns = np.append(posns, posn)
        cams = np.append(cams, cam)
        minsVec = np.append(minsVec, minsF)
        minsFAll = pd.concat([minsFAll, pd.DataFrame(minsF)], ignore_index=True, axis=1)   
        trait1FAll = pd.concat([trait1FAll, pd.DataFrame(trait1)], ignore_index=True, axis=1)
        trait2FAll = pd.concat([trait2FAll, pd.DataFrame(trait2)], ignore_index=True, axis=1)

    minsVect = np.int64(np.unique(minsVec))
    minsFAll.columns = posns
    trait1FAll.columns = posns
    trait2FAll.columns = posns
    locat['posn'] = posns
    locat['camera'] = cams

    return minsFAll, trait1FAll, trait2FAll, minsVect, locat

#%%
def timeAdjust(minutes, dayInt, dayFnl, increm_min):
    start = dayInt * (24 * 60)
    final = dayFnl * (24 * 60)
    step = increm_min
    vecTime = np.arange(start, 120 * (24 * 60), step)
    
    time = []
    for cnt in range(len(minutes)):
        ind, timeAux = [], []
        t = minutes[cnt]
        ind = np.argmin(np.abs(vecTime - t))
        timeAux = vecTime[ind]
        
        if timeAux <= final:
            time = np.append(timeAux, time)
    mins = np.sort(time)
    return mins



#%%
def seriesOriginal(minsAll, trait1All, trait2All, minsVect, locat, dayST):
    missing, total = 0, 0
    trait1Series, trait2Series = pd.DataFrame([]), pd.DataFrame([])
    trait1Mean, trait1STD, trait1Var, trait1MeanFit = [], [], [], []
    trait2Mean, trait2STD, trait2Var, trait2MeanFit = [], [], [], []
    
    posns = locat.loc[:, 'posn']
    positions = minsAll.columns
    nanVal = np.copy(minsVect.astype(np.float32))
    nanVal[:]= 0

    for posn in positions:
        mins, minsAux, index = [], [], []
        trait1, trait1Aux , trait2, trait2Aux = [], [], [], []

        trait1Repl = np.copy(minsVect.astype(np.float32))  
        trait2Repl = np.copy(minsVect.astype(np.float32))
        trait1Repl[:]= 0
        trait2Repl[:]= 0
        trait1Aux = trait1All.loc[:, posn].values
        trait2Aux = trait2All.loc[:, posn].values
        minsAux = minsAll.loc[:, posn].values        
        indAux = np.argwhere(~np.isnan(minsAux))  
        
        for cntIn in range(len(indAux)): index.append(indAux[cntIn][0])
        
        mins = minsAux[index]
        trait1 = trait1Aux[index]
        trait2 = trait2Aux[index]
        trait1Repl[:] = 0
        trait2Repl[:] = 0
        total+= len(minsVect)
        missing+= len(minsVect) - len(mins)
        
        for cnt2 in range(len(mins)):
            trt1, trt2, Vect_ind = [], [], []
            Vect_ind = np.where(minsVect == mins[cnt2])[0]
            
            if len(Vect_ind) == 0: continue
            
            trt1 = trait1[cnt2]
            trt2 = trait2[cnt2]
            trait1Repl[Vect_ind] = trt1
            trait2Repl[Vect_ind] = trt2

        trait1Series.loc[:, posn] = trait1Repl
        trait2Series.loc[:, posn] = trait2Repl
    
    trait1Series[trait1Series == 0] = np.nan
    trait1Mean = trait1Series.mean(axis=1)
    trait1STD = trait1Series.std(axis=1)
    trait1Var = trait1Series.var(axis=1) 
    trait2Series[trait2Series == 0] = np.nan
    trait2Mean = trait2Series.mean(axis=1)
    trait2STD = trait2Series.std(axis=1)
    trait2Var = trait2Series.var(axis=1) 

    intCond = [1e-5, 1e-5]
    [a,b], pcov = curve_fit(stoll, minsVect, trait1Mean.values, intCond)
    trait1MeanFit = stoll(minsVect,a,b)  
    
    trait2MeanFit = trait2Mean
    seconds = minsVect * 60
    dateAux = pd.to_datetime(seconds, unit='s', origin=pd.Timestamp(dayST))
    date = (((dateAux.to_frame()).reset_index())['index']).to_frame()
    date.rename(columns={'index':'time'},inplace=True)
    
    trait1Series = pd.concat([trait1Series, date], ignore_index=False, axis=1)
    trait1Series['mins'] = minsVect
    trait1Series['mean'] = trait1Mean
    trait1Series['STD'] = trait1STD
    trait1Series['var'] = trait1Var
    trait1Series['meanFit'] = trait1MeanFit

    trait2Series = pd.concat([trait2Series, date], ignore_index=False, axis=1)
    trait2Series['mins'] = minsVect
    trait2Series['mean'] = trait2Mean
    trait2Series['STD'] = trait2STD
    trait2Series['var'] = trait2Var
    trait2Series['meanFit'] = trait2MeanFit

    columns = trait1Series.columns.tolist()
    columns = columns[-6:] + columns[:-6]
    
    trait1Series = trait1Series[columns]
    trait1Series = trait1Series.drop_duplicates(subset = 'mins')
    trait1Series = trait1Series.reset_index(drop=True)
    
    trait2Series = trait2Series[columns]
    trait2Series = trait2Series.drop_duplicates(subset = 'mins')
    trait2Series = trait2Series.reset_index(drop=True)

    return trait1Series, trait2Series

#%%
def minsVector(hourStar, hourStop, minP):
    tmeVect = pd.date_range(hourStar, hourStop, freq = minP).to_frame()
    tmeVect.reset_index(drop=True, inplace=True)
    tmeVect.columns = ['time']
    tmeVect['HHMM'] = tmeVect['time'].dt.time
    tmeVect.drop(columns = ['time'], inplace=True)
    
    return tmeVect

#%%
def seriesDownSampl(inputSeries, tmeVect, daySowing):
    df = inputSeries.copy()
    df['time'] = df.index
    df['date'] = df['time'].dt.date
    df['days'] = ((df['time'] - daySowing).dt.total_seconds())/(60*60*24)
    df['HHMM'] = df['time'].dt.time
    df.reset_index(drop=True, inplace=True)
    df = df[df['HHMM'].isin(tmeVect['HHMM'])]
    df.reset_index(drop=True, inplace=True)
    df.index = df['time']
    
    
    posns = list(filter(lambda x: (x[0] == 'T'), df.columns.tolist())) 
    for posn in posns:
       daysTrait = df[['days', posn]]
       days = daysTrait.loc[:, 'days'].values
       trait = daysTrait.loc[:, posn].values
       # fig, Adj = plt.subplots(1, 1, figsize=(12,12))
       # Adj.plot(days, trait, label = posn)
       # Adj.set_title(str(posn),  fontsize=20)
       # Adj.legend(loc='upper left', shadow=True, fontsize= 24, edgecolor = 'Indigo')
    
    df.drop(columns = ['time', 'date', 'days', 'HHMM'], inplace=True)
   
    return df

#%%
def calcShift(inputSeries, feature, daySowing, leafNum, offDay):
    shiftMtx = pd.DataFrame(columns=['posn', 'shiftDay'])
    offSft = 0
    
    df = inputSeries.copy()
    posns = list(filter(lambda x: (x[0] == 'T'), df.columns.tolist())) 
    
    df['mean'] = df.loc[:, posns].mean(axis =1)
    df['time'] = df.index
    df['date'] = df['time'].dt.date
    df['HHMM'] = df['time'].dt.time
    df['days'] = ((df['time'] - daySowing).dt.total_seconds())/(60*60*24)
    
    if feature == 'leaf':
        daysLim = df.loc[df['mean'] <= leafNum, 'days'].max()
        df = df[df['days']< daysLim +1]

    df.reset_index(drop=True, inplace=True)

    dfmin = df['days'].min()
    dfmax = df['days'].max()
    
    intCond = [1e-5, 1e-5]
    [aStolMed, bStolMed], pcov = curve_fit(stoll, df['days'].values, df['mean'].values, intCond)
    tFit = stoll(df['days'].values, aStolMed, bStolMed)

    
    for posn in posns:
        daysTrait = df[['days', posn]]
        shiftTrait, smin, smax = [], [], []
        MSE = pd.DataFrame(columns=['mse', 'shift', 'abs'])
        offIdx = 0
        
        # fig, Adj = plt.subplots(1, 1, figsize=(12,12))
        # Adj.plot(df['days'].values, tFit, color ='red', label = 'fit')
        # Adj.plot(df['days'].values, df['mean'].values, color ='red', label = 'mean')
        # Adj.plot(df['days'].values, df[posn].values, color ='blue', label = posn)
        
        for off in range(-offDay, offDay, 1):
            mse = []
            shiftTrait = daysTrait.copy()
            shift = shiftTrait.loc[:, 'days'].values + off
            shiftmin =  shift.min()
            shiftmax =  shift.max()
            shiftTrait.loc[:, 'days'] = shift
            shiftTrait = shiftTrait.reset_index(drop=True)
            
            [aStol, bStol], pcov = curve_fit(stoll, shift, shiftTrait[posn].values, intCond)
            traitFit = stoll(shift, aStol, bStol)
            traitMedFit = stoll(shift, aStolMed, bStolMed)

            N= len(traitFit)
            mse = np.mean(((traitFit- traitMedFit))**2)/N
            MSE.loc[offIdx, 'mse'] = mse
            MSE.loc[offIdx, 'shift'] = off
            MSE.loc[offIdx, 'abs'] = np.abs(off)
            offIdx += 1
            
            # Adj.plot(shift, traitFit, label = posn + ' ' + 'Error=' + str(format((mse),'.2f'))+ ' day off= ' + str(off) + ' length=' + str(len(shiftTrait)))
            # Adj.legend(loc='upper left', shadow=True, fontsize= 12, edgecolor = 'Indigo')
            
        MSEsort = MSE.sort_values(['mse', 'abs'], ascending=[True, True])
        MSEsort.reset_index(drop=True, inplace=True)
        sday = MSEsort.loc[0, 'shift']

        shiftMtx.loc[offSft, 'posn'] = posn
        shiftMtx.loc[offSft, 'shiftDay'] = sday
        offSft += 1

        moveTrait = df[['days', posn]]
        move = moveTrait.loc[:, 'days'].values + sday
        moveTrait.loc[:, 'days'] = move
        moveTrait = moveTrait[(moveTrait['days'] >= dfmin) & (moveTrait['days'] <= dfmax)]
        moveTrait.reset_index(drop=True, inplace=True)
        moveTraitmin = moveTrait.loc[:, 'days'].min()
        moveTraitmax = moveTrait.loc[:, 'days'].max()
        index = np.where((df['days'] >= moveTraitmin) & (df['days'] <= moveTraitmax))[0]
        df.loc[:, posn] = np.nan
        df.loc[index, posn] = moveTrait.loc[0:len(index) - 1, posn].values
        
        # Adj.set_title('The lowest shiftDay= ' + str(sday),  fontsize=20)
        # Adj.plot(df.loc[:, 'days'].values, df.loc[:, posn].values, color ='cyan')
        # Adj.legend(loc='upper left', shadow=True, fontsize= 24, edgecolor = 'Indigo')
        
        # print(10*'-')
        # print(MSEsort)
        # print( dfmin,  dfmax, moveTrait.loc[:, 'days'].min(), moveTrait.loc[:, 'days'].max())
        # print('length of the index = ', len(index))
    
    df.set_index(pd.DatetimeIndex(df['time']), inplace=True)
    df.drop(columns = ['time', 'date', 'HHMM', 'days', 'mean'], inplace = True)
    
    return df, shiftMtx  

#%%
def timeShift(inputSeries, posns, daySowing, shiftMtx):
    df = inputSeries.copy()
    df['mean'] = df.loc[:, posns].mean(axis =1)
    df['time'] = df.index
    df['date'] = df.loc[:,'time'].dt.date
    df['HHMM'] = df.loc[:,'time'].dt.time
    df['days'] = ((df.loc[:,'time'] - daySowing).dt.total_seconds())/(60*60*24)
    df.reset_index(drop=True, inplace=True)
    dfmin = df.loc[:, 'days'].min()
    dfmax = df.loc[:, 'days'].max()
 
    for posn in posns:
        sday = shiftMtx.loc[shiftMtx.loc[:,'posn'] == posn, 'shiftDay'].values

        # fig, Adj = plt.subplots(1, 1, figsize=(12,12))
        # Adj.plot(df['days'].values, tFit, color ='red', label = 'fit')
        # Adj.plot(df['days'].values, df['mean'].values, color ='red', label = 'mean')
        # Adj.plot(df['days'].values, df[posn].values, color ='blue', label = posn)

        moveTrait = df[['days', posn]]
        move = moveTrait.loc[:, 'days'].values + sday
        moveTrait.loc[:, 'days'] = move
        moveTrait = moveTrait[(moveTrait['days'] >= dfmin) & (moveTrait['days'] <= dfmax)]

        index = ((df['days'] >= moveTrait.loc[:, 'days'].min()) & (df['days'] <= moveTrait.loc[:, 'days'].max()))
        df.loc[:, posn] = np.nan
        df.loc[index, posn] = moveTrait.loc[:, posn].values
        
        # Adj.set_title('The lowest shiftDay= ' + str(sday),  fontsize=20)
        # Adj.plot(df.loc[:, 'days'].values, df.loc[:, posn].values, color ='cyan')
        # Adj.legend(loc='upper left', shadow=True, fontsize= 24, edgecolor = 'Indigo')
        
        # print(10*'-')
        # print(MSEsort)
        # print( dfmin,  dfmax, moveTrait.loc[:, 'days'].min(), moveTrait.loc[:, 'days'].max())
        # print('length of the index = ', len(index))
    
    df.set_index(pd.DatetimeIndex(df['time']), inplace=True)
    df.drop(columns = ['time', 'date', 'HHMM', 'days', 'mean'], inplace = True)
    
    return df
#%%

def STATS(traitSeries, posns, dayS):
    traitSeries['time'] = traitSeries.index
    traitSeries['days'] = ((traitSeries['time'] - dayS).dt.total_seconds())/(60*60*24)
    traitSeries['mean'] = traitSeries.loc[:, posns].mean(axis = 1) 
    traitSeries['STD'] = traitSeries.loc[:, posns].std(axis = 1) 
    traitSeries['var'] = traitSeries.loc[:, posns].var(axis = 1) 
    subSeries = traitSeries[['days', 'mean']]
    subSeries = subSeries.dropna()
    intCond = [1e-5, 1e-5]
    [a,b], pcov = curve_fit(stoll, subSeries['days'].values, subSeries['mean'].values, intCond)
    traitSeries['meanFit'] = stoll(traitSeries['days'].values,a,b)

    return traitSeries  

#%%

