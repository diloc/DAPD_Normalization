# DAPD Method
Digital Adjustment of Plant Development (_DAPD_) is a method that synchronizes shoot phenotypic measurements. It uses the plant leaf number to normalizes time-series measurements, such as the projected rosette area and leaf area. This method improves accuracy by decreasing the statistical dispersion of time-series of quantitative traits _(Figure 1)_. Also, it can identify more outliers than any other central tendency technique on the non-normalized dataset. The DAPD method was written in Python programming language and presented in Juptyter notebook pages.


<figure>
  <img src="https://github.com/diloc/DAPD_Normalization/blob/master/results_Col-0.jpg">
  <figcaption>
  Figure 1: Mean and standard deviation of the non-normalized and normalized projected rosette area datasets. (a) the non-normalized datasets of Col-0 plants in experiment 1, (b) the normalized datasets of Col-0 plants in experiment 1. The light purple band indicates the standard deviation and the solid blue curve indicates the mean area.
  </figcaption>
</figure>

## Description
The DAPD method uses image processing algorithms to analyze and extract plant phenotyping traits. It starts by loading RGB images and other files such as camera parameters which are used to correct the lens distortion. After, the image quality is improved by reducing the noise and correcting the color distortion. Then, the projected rosette is segmented from the pot image by removing automatically the background. Finally, phenotyping traits are obtained from the segmented image and write in CSV files. The traits include projected rosette area, leaf number, and perimeter _(Figure 2)_. The user can run DAPD image processing module to extract the traits (See tutorial).

<figure>
  <img src="https://github.com/diloc/DAPD_Normalization/blob/master/ImProcess_Steps.png">
  <figcaption>
  Figure 2: The most important image processing steps: Acquisition, correction and noise reduction, pot cropping, image segmentation and phenotyping measurements.
  </figcaption>
</figure>



The time-series of phenotyping traits are normalized to an early plant development stage. The number of leaves is used to identify a particular development stage among plants in an experiment (HTP scale). Then, the relationship between the development stages and time-series is studied by shifting the series timeline and calculating the regression.



After applying the image processing algorithms, phenotyping traits are measured during the acquisition time and stored in a CSV file (Table 1).

|Phenotyping Traits|
|----------|
|Projected rosette area|
|Hull Area|
|Radius|
|Roundness|
|Compactness|
|Eccentricity|

