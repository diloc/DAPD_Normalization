import numpy as np
from scipy.optimize import curve_fit



#%% Fitting kernels
def stoll(t,a,b):
    return (a* np.exp(t*b))

def stoll2(t,a,b,c):
    return (a* np.exp(t*b)+c*t)

def gompertz(t,a,b,c):
    return a*(np.exp(-b*(np.exp(-c*t) )))

def richard(t,a,b,c):
    return a*((1-np.exp(-b*t))**c)

def logistic(t,a,b,c):
    return a*np.power((1+c*np.exp(-b*t) ),-1)

#%% Model selection
def model(time,area, timeFit, model):
    if model=='stol':
        intCond = [1e-2, 1e-2]
        [a,b], pcov = curve_fit(stoll, time, area,intCond)
        areaF= stoll(timeFit,a,b)
        param= [a,b]
        perr = np.sum((area - stoll(time,a,b))**2) / len(area)
#        perr = np.sqrt(np.diag(pcov))
    
    if model=='stol2':
        intCond = [1e-2, 1e-2, 1e-2]
        [a,b,c], pcov = curve_fit(stoll2, time, area,intCond)
        areaF= stoll2(timeFit,a,b,c)
        param= [a,b,c]
        
        perr = np.sum((area - stoll2(time,a,b,c))**2) / len(area)
#        perr = np.sqrt(np.diag(pcov))
    
    if model=='gompertz':
        intCond = [50, 1e-2, 1e-2]
        [a,b,c], pcov = curve_fit(gompertz, time, area,intCond)
        areaF= gompertz(timeFit,a,b,c)
        param= [a,b,c]
        perr = np.sqrt(np.diag(pcov))
    
    if model=='richard':
        intCond = [1e-2, 1e-2, 1e-2]
        [a,b,c], pcov = curve_fit(richard, time, area,intCond)
        areaF= richard(timeFit,a,b,c)
        param= [a,b,c]
        perr = np.sqrt(np.diag(pcov))
    
    if model=='logistic':
        intCond = [1e-2, 1e-2, 1e-2]
        [a,b,c], pcov = curve_fit(logistic, time, area,intCond)
        areaF= logistic(timeFit,a,b,c)
        param= [a,b,c]
        perr = np.sqrt(np.diag(pcov))

    return timeFit, areaF, param, perr





#%%
# R-squared is for linear models
    
def r_squared(x,y,n):
    num=n*np.sum(x*y)-(np.sum(x))*(np.sum(y))
    den=np.sqrt((n*np.sum(x**2)-(np.sum(x)**2))*(n*np.sum(y**2)-(np.sum(y)**2)))
    rs=num/den
    return rs



