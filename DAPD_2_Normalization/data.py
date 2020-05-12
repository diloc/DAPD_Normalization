# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 16:09:55 2018

@author: dlozano
"""
import pandas as pd
import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

def raw (csvPath,dayInt,dayFnl):
    df = pd.read_csv(csvPath)
    df=df.sort_values(by=['mins'])
    df1 = df.loc[(df["mins"] >= dayInt*(24*60)) & (df["mins"] <= dayFnl*(24*60)) ]
    mins = pd.Series(df1.mins).values
    days=mins/(24*60)
    area = pd.Series(df1.area).values
    leafNum = pd.Series(df1.lNumGeo).values
    
    return days, area, leafNum


def timeVector(pth):
    path = pth.tolist()
    days = []
    for cnt in range(len(path)):
        csvPath = path[cnt]
        df = pd.read_csv(csvPath)
        df=df.sort_values(by=['mins'])
        day = pd.Series(df.mins /(24*60)).values
        days = np.concatenate((days, day), axis=0)
    daysAll = np.unique(days)
    return daysAll


def table(labelAllName, csvAllName):
    df = pd.DataFrame(csvAllName)
    df.columns = ['folder','file']
    aux1 = df['file'].str.split("_T", n = 1, expand = True)
    aux2 = aux1[1].str.split("_", n = 3, expand = True)
    df['ecotype'] = aux1[0]
#    df['tray'] = aux2[0]
#    df['loc'] = aux2[1]
    df['posn'] = 'T' +aux2[0] + '_' + aux2[1]
    df['camera'] = aux2[2].str.split(".", n = 1, expand = True)[0]
    df['status'] = ''
    df['outlier'] = ''
    for cnt in range(len(df)):
        name = df['file'].str.split("_cam", n = 1, expand = True)[0][cnt]
        idx = np.where(labelAllName[0].values== name)
        statIDX = labelAllName[1][idx[0]].values[0]
        df['status'][cnt] = statIDX
        outIDX = labelAllName[2][idx[0]].values[0]
        df['outlier'][cnt] = outIDX
    
    table = df.drop_duplicates(subset=['posn'], keep="first")
    table = table.sort_values(by=['posn'])
    table.reset_index(drop=True)
    return table

def curves(df, curvesCSV):
    dayAll = timeVector(df['folder'] + df['file'])
    curves = pd.DataFrame({'time':[]})
    curves['time'] = dayAll
    dayAll = np.resize(dayAll,(len(dayAll),1))
  
    ecotypes = df.ecotype.unique()
    status = df.status.unique()
    
    for cnt in range(len(ecotypes)):
        ecotype=ecotypes[cnt]
        idx = np.where(df['ecotype'].values== ecotype)
        ecos = df.iloc[idx]
        ecos = ecos.reset_index(drop=True)
        for cnt2 in range(len(status)):
            stat = status[cnt2]
            idy = np.where(ecos['status'].values== stat)
            ecosF = ecos.iloc[idy]
            ecosF = ecosF.reset_index(drop=True)
            out = ''
            for cnt3 in range(len(ecosF)):
                csvPath = ecosF['folder'][cnt3] + ecosF['file'][cnt3]
                place = ecosF['posn'][cnt3]
                cam = ecosF['camera'][cnt3]
                out = ecosF['outlier'][cnt3]
                daysOld,areaOld, leavesOld = raw(csvPath,0,60)
                idc = np.where(dayAll == daysOld)[0]
                curves.loc[idc, ecotype + ' ' + 'area'+'_'+ place + '_'+ stat+'_'+cam+'_'+out]= areaOld
                curves.loc[idc, ecotype + ' ' + 'leaves'+'_'+ place + '_'+ stat+'_'+cam+'_'+out]= leavesOld
    curves.to_csv (curvesCSV, index = None, header=True)
    return curves
    

def separFrames(curves):
    df = pd.DataFrame(list(curves.columns.values))
    df = df.drop([0, 0])
    df.columns = ['name']
    
    
    aux1 = df['name'].str.split(" ", n = 2, expand = True)
    aux2 = aux1[1].str.split("_", n = 5, expand = True)
    df['ecotype'] = aux1[0]
    df['posn'] = aux2[1] + '_' + aux2[2]
    df['tray'] = aux2[1]
    df['trait'] = aux2[0]
    df['status'] = aux2[3]
    df['camera'] = aux2[4]
    df['outlier'] = aux2[5]
    idz = np.where(df['trait'].values== 'area')
    df1 = df.iloc[idz]
    df1 = df1.reset_index(drop=True)
    
    idp = np.where(df['trait'].values== 'leaves')
    df2 = df.iloc[idp]
    df2 = df2.reset_index(drop=True)
    
    return df1, df2
    
def AGR(daysR,areaR,samp):
    daysI = np.unique(np.int16(daysR))
    daySamp = np.array(samp)/24
    dayCur, areaCur = [], []
    
    for cntInt in daysI:
        for cntDayC in daySamp:
            DayC = cntInt + cntDayC
            indayC = (np.abs(daysR - DayC)).argmin()
            dayCur.append(daysR[indayC])
            areaCur.append(areaR[indayC])

    dayCur = np.array(dayCur)
    areaCur =  np.array(areaCur)    
    areaAGR = np.diff(areaCur)/np.diff(dayCur)
    dayAGR = dayCur[:-1]
    return dayAGR, areaAGR

def RGR(daysR,areaR,samp):
    daysI = np.unique(np.int16(daysR))
    daySamp = np.array(samp)/24
    dayCur, areaCur = [], []
    
    for cntInt in daysI:
        for cntDayC in daySamp:
            DayC = cntInt + cntDayC
            indayC = (np.abs(daysR - DayC)).argmin()
            dayCur.append(daysR[indayC])
            areaCur.append(areaR[indayC])

    dayCur = np.array(dayCur)
    areaCur =  np.array(areaCur)   
    areaRGR =  (np.log(areaCur[1:]) - np.log(areaCur[0:-1])) / (dayCur[1:] - dayCur[0:-1])
    dayRGR = dayCur[:-1]
    return dayRGR, areaRGR



def padding(dayFit,days1,area1):
    idcon1 = np.where(dayFit<np.min(days1))
    idcon2 = np.where(dayFit>np.max(days1))
    areaBelow = np.empty(np.size(idcon1))
    areaBelow[:] = np.nan
    areaAbove = np.empty(np.size(idcon2))
    areaAbove[:] = np.nan
    
#    areaBelow = np.min(area1)*np.ones(np.size(idcon1))
#    areaAbove = np.max(area1)*np.ones(np.size(idcon2))
    days2 = np.concatenate((dayFit[idcon1], days1,dayFit[idcon2]),axis=0)
    area2 = np.concatenate((areaBelow, area1,areaAbove),axis=0)
    return days2, area2

def padding2(dayFit,days1,area1):
    idcon1 = np.where(dayFit<np.min(days1))
    idcon2 = np.where(dayFit>np.max(days1))
    areaBelow = np.min(area1)*np.ones(np.size(idcon1))
    areaAbove = np.max(area1)*np.ones(np.size(idcon2))
    areaAbove[:] = np.nan
    

    days2 = np.concatenate((dayFit[idcon1], days1,dayFit[idcon2]),axis=0)
    area2 = np.concatenate((areaBelow, area1,areaAbove),axis=0)
    return days2, area2

def upsampling(days2,area2, dayInt, dayFnl, samples):
    f = interpolate.interp1d(days2,area2)
    daysR = np.linspace(dayInt+0.01,dayFnl-0.01, samples)
    areaR = f(daysR)
    return daysR, areaR


def filtering(days, area, model, window, degree):
    if model == 'savgol':
        areaFil = savgol_filter(area, window, degree)
        
    return days, areaFil
    

    