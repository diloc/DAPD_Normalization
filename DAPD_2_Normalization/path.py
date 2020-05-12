import os
import sys
import numpy as np
import glob
import pandas as pd



def directories(location,experiment,compName):
    if (len(location)==1) and (location=='cloud'):
        root = 'C:/Users/dlozano/OneDrive - LA TROBE UNIVERSITY/Image_Processing_Programs/images/'
        inputfolder=root+'/'
        
    #if (location=='local')and (compName=='GQQ4YC2'):
    if (len(location)==2) and (location[0]=='local'):
        root=location[1]+experiment +'/'
        inputfolder=root+experiment+'_0003/'+'/'

    return root,inputfolder



def files(inputfolder):
    folders = os.listdir(inputfolder)
    csvAllName = []
    for cnt in range(len(folders)):
        inputF = inputfolder + folders[cnt] + '/'
        for file in os.listdir(inputF):
            if file.endswith(".csv"): csvAllName.append([inputF, file])
        csvAllName.sort()
    return csvAllName


# def files2(inputfolder, ext):
#     df  = pd.DataFrame(columns = ['folder', 'file'])
    
#     for file in os.listdir(inputfolder):
#         if file.endswith(ext):
#             df  =  df.append({'folder':inputfolder, 'file':file}, ignore_index=True)
            
#     return df

def files2(inputfolder, star):
    df  = pd.DataFrame(columns = ['folder', 'file'])
    
    for file in os.listdir(inputfolder):
        if file.startswith(star):
            df  =  df.append({'folder':inputfolder, 'file':file}, ignore_index=True)
            
    return df


def filesEnd(inputfolder, endwith):
    csvAllName = []
    for file in os.listdir(inputfolder):
        if file.endswith(endwith): csvAllName.append(file)
    csvAllName.sort()
    return csvAllName