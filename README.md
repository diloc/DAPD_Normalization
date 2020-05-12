# DAPD Method
Digital Adjustment of Plant Development (_DAPD_) is a method that synchronizes shoot phenotypic measurements. It uses the plant leaf number to normalizes time-series measurements, such as the projected rosette area and leaf area. This method improves accuracy by decreasing the statistical dispersion of time-series of quantitative traits. Also, it can identify more outliers than any other central tendency technique on the non-normalized dataset.

## The DAPD modules: 
The DAPD method has two modules that are used to process information, including raw images of plants, and datasets (.csv). These modules were written in Python programming language and presented in Juptyter notebook pages. 
- __Rosette and leaf segmentation module__ uses multiple image processing algorithms to extract the rosette area and remove the background from plant images. The leaf segmentation extracts individual leaf from the rosette. 
- __Normalization module__ calculates a reference time-line using cross-correlation at multiple time points of the time-series measurements, which include rosette area, leaf size, and number.
## Data files:
The source files are images of plant trays, and each one can allocate 20 pots, which are uniformly distributed _(Figure 1)_. Each pot has an individual plant that can be from the same or a different __Arabidopsis thaliana__ line/mutant.   

<figure>
  <img src="https://github.com/diloc/DAPD_Normalization/blob/master/2017-11-27-15-35_T06_cam03.jpg">
  <figcaption>
  Figure 1: An image of a tray with 20 pots
  </figcaption>
</figure>

After applying the image processing algorithms, phenotyping traits are measured during the acquisition time (Table 1).

|Phenotyping Traits|
|----------|
|Projected rosette area|
|Hull Area|
|Radius|
|Roundness|
|Compactness|
|Eccentricity|

