# DAPD Method
Digital Adjustment of Plant Devopment (_DAPD_) is a method that sychronize shoot phenotypic measurements. It uses the plant leaf number to normalizes time-series measurements such as the projected rosette area and leaf area. This method improves accuracy by decreasing the statistical dispersion of time-series of quantitative traits. Also, it can identify more outliers than any other central tendency technique on the non-normalised dataset.

## The DAPD modules: 
The DAPD method has three modules which are used to process information including raw images of plants, and datasets (.csv): 
- __Rosette segmentation module__ uses multiple image processing algorithms to extract the rosette area and remove the background from plant images. 
- __Leaf segmentation module__  extracts individual leaf from the rosette. 
- __Normalization module__ calculates a reference time-line using cross-correlation at multiple time points of the time-series measurements, which include rosette area, leaf size and number.
## Data files:
The source files are images of plant trays and each one can allocate 20 pots uniform distributed _(fig. 1)_. 
![GitHub Logo](/images/logo.png) Format: ![Alt Text](url)




