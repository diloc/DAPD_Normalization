# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 21:58:28 2018

@author: dlozano
"""
import numpy as np
import os
import csv
import cv2
import pandas as pd
import glob
#%%
def  curve(fileID,root,rosSig):   
    potName,cntRow,cntCol,trayName,cam,experiment,mins,dateF = fileID
    
    data=np.concatenate(([mins],rosSig))
    
    pathCVS=root+experiment+'_0004/'+cam+'/' 
    if not os.path.exists(pathCVS):
        os.makedirs(pathCVS)
        
    filetext='.csv'
    filepath= pathCVS+potName+'_'+trayName+'_'+cntRow+cntCol+'_'+cam+filetext

    if not os.path.isfile(filepath):
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow(data)  
    else:
         with open(filepath, 'a') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow(data)           
    csvfile.close()



#%%
#def  CVS(fileID,root,area,rosPheno,issue,lNumWaSh,lNumGeo):   
#    
#    potName,cntRow,cntCol,trayName,cam,experiment,mins,dateF = fileID
#    length,hullArea,roundness,roundness2,compact,eccentricity,radius = rosPheno
#    
#    pathCVS=root+experiment+'_0003/'+cam+'/' 
#    if not os.path.exists(pathCVS):
#        os.makedirs(pathCVS)
#        
#    filetext='.csv'
#    filepath= pathCVS+potName+'_'+trayName+'_'+cntRow+cntCol+'_'+cam+filetext
#    
#    
#    if not os.path.isfile(filepath):
#        with open(filepath, 'w') as csvfile:
#            fieldnames = ['mins','area','time','Arc_lenght','hullArea','radius','roundness','roundness2','compact','eccentricity','lNumWaSh','lNumGeo','issue']
#            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#        
#            writer.writeheader()
#    
#            writer.writerow({'mins':mins,'area':area,'time':dateF,'Arc_lenght':length,'hullArea':hullArea,'radius':radius,'roundness':roundness,\
#                             'roundness2':roundness2,'compact':compact,'eccentricity':eccentricity,\
#                             'lNumWaSh':lNumWaSh,'lNumGeo':lNumGeo,'issue':issue})
#    else:
#         with open(filepath, 'a') as csvfile:
#            fieldnames = ['mins','area','time','Arc_lenght','hullArea','radius','roundness','roundness2','compact','eccentricity','lNumWaSh','lNumGeo','issue']
#            writer = csv.writer(csvfile, dialect='excel')
#            writer.writerow([mins,area,dateF,length,hullArea,radius,roundness,roundness2,compact,eccentricity,lNumWaSh,lNumGeo,issue])           
#    csvfile.close()

#%%
def imOrig(fileID,root,imOrig):
    
    potName, posn, trayName, cam, EXP, mins, dateF, leaf = fileID
    pathIm=root+EXP+'_0002/'+cam+'/' 
    potFolder=pathIm+potName+'_'+trayName+'_'+ posn +'_'+cam+'/'
    potOrig =potFolder+'pot/'
    
    dateIm = dateF.strftime("%Y-%m-%d-%H-%M")
    
    imName  = dateIm +'_'+ potName+ '_' + trayName + posn + '_' + 'leaf' + str(leaf) + '.jpg'
    # imName  = str(format(np.int32(mins),'06d'))+'_'+ potName+ '_' + trayName + posn + '_' + 'leaf' + str(leaf) + '.jpg'
    if not os.path.exists(potOrig):  os.makedirs(potOrig)
    cv2.imwrite(os.path.join(potOrig,imName),imOrig, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

def imSegm(fileID,root,imSegm):

    potName, posn, trayName, cam, EXP, mins, dateF, leaf = fileID
    pathIm=root+EXP+'_0002/'+cam+'/' 
    potFolder=pathIm+potName+'_'+trayName+'_'+posn+'_'+cam+'/'
    potSegm =potFolder+'segment/'
    dateIm = dateF.strftime("%Y-%m-%d-%H-%M")
    
    
    imName  = dateIm +'_'+ potName+ '_' + trayName + posn + '_' + 'leaf' + str(leaf) + '.jpg'
    # imName  = str(format(np.int32(mins),'06d'))+'_'+ potName+ '_' + trayName + posn + '_' + 'leaf' + str(leaf) + '.jpg'
    
    if not os.path.exists(potSegm):  os.makedirs(potSegm)
    cv2.imwrite(os.path.join(potSegm,imName),imSegm, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

def imWaSh(fileID,root,imWaSh):

    potName, posn, trayName, cam, EXP, mins, dateF = fileID
    pathIm=root+EXP+'_0002/'+cam+'/' 
    potFolder=pathIm+potName+'_'+trayName+'_'+ posn +'_'+cam+'/'
    potWaSe =potFolder+'watershed/'
    imName  = str(format(np.int32(mins),'07d'))+'_'+potName+'_'+trayName+'_'+ posn +'.jpg'
    if not os.path.exists(potWaSe):  os.makedirs(potWaSe)
    cv2.imwrite(os.path.join(potWaSe,imName),imWaSh, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


def  centroid(root, EXP, cam, trayName, posn, mins, ctRow, ctCol):   
    pathCVS= root+ EXP + '_' +'centroids' +'/' + cam + '/' 
    if not os.path.exists(pathCVS):
        os.makedirs(pathCVS)
        
    filetext='.csv'
    filepath= pathCVS + trayName + '_' + posn + filetext
    
    if not os.path.isfile(filepath):
        df = pd.DataFrame({'mins': [mins],'ctRow':[ctRow],'ctCol':[ctCol]})
        df.to_csv(filepath,  sep=',', index=False)
        ctRowM = ctRow
        ctColM = ctCol
        
    else:
        df = pd.read_csv(filepath)
        df1 = pd.DataFrame({'mins': [mins],'ctRow':[ctRow],'ctCol':[ctCol]})
        df2 =  pd.concat([df, df1], ignore_index=True)
        df3 = df2.drop_duplicates()
        ctRowM = np.int(df3["ctRow"].mean())
        ctColM = np.int(df3["ctCol"].mean())
        df3.to_csv(filepath,  sep=',', index=False)
        
    return ctRowM, ctColM


def  CVS(fileID, pathCVS, area, rosPheno,leaf):   
    
    potName, posn, trayName, cam, EXP, mins, dateF = fileID
    length,hullArea,roundness,roundness2,compact,eccentricity,radius = rosPheno
    
    # pathCVS=root+EXP+'_0003/'+cam+'/' 
    if not os.path.exists(pathCVS):
        os.makedirs(pathCVS)
        
    # filetext='.csv'
    # filepath= pathCVS + potName + '_' + trayName + '_' +posn + '_' + cam + filetext
    filepath= os.path.join(pathCVS, potName + '_' + trayName + '_' +posn + '_' + cam + '.csv') 
   
    if not os.path.isfile(filepath):
        df = pd.DataFrame({'mins':[mins],'area':[area],'time':[dateF],'Arc_lenght':[length],'hullArea':[hullArea],'radius':[radius],'roundness':[roundness],\
                             'roundness2':[roundness2],'compact':[compact],'eccentricity':[eccentricity],\
                             'leaf':[leaf]})
        df.to_csv(filepath,  sep=',', index=False)

    else:
        df = pd.read_csv(filepath)
        df1 = pd.DataFrame({'mins':[mins],'area':[area],'time':[dateF],'Arc_lenght':[length],'hullArea':[hullArea],'radius':[radius],'roundness':[roundness],\
                             'roundness2':[roundness2],'compact':[compact],'eccentricity':[eccentricity],\
                             'leaf':[leaf]})
        df2 =  pd.concat([df, df1], ignore_index=True)
        df3 = df2.drop_duplicates()
        df3.to_csv(filepath,  sep=',', index=False)


def remove(root, EXP, folder, cam):   
    pathCVS= root+ EXP + '_' + folder +'/' + cam + '/' 
    
    filelist = glob.glob(os.path.join(pathCVS, "*.*"))
    for f in filelist:
        os.remove(f)