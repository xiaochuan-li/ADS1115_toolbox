# ADS1115_toolbox
  This is a toolbox for ADS1115, including the functions for configuring for and reading from a ADS1115, and an example using a magnetic field sensor to measure the distance.

## 0. Intriduction to the Parameters of ADS1115
  To read from ADS1115, we must first write a configuration of two bytes into it. (see the table below)  
  ++++TABLE FOR AIN(AIN4=GND)++++  
  +++++++++++++++++++  
  | CODE (10) |  CODE (2) | AINP | AINN |  
|     0     |    000    | AIN0 | AIN1 |  
|     1     |    001    | AIN0 | AIN3 |  
|     2     |    010    | AIN1 | AIN3 |  
|     3     |    011    | AIN2 | AIN3 |  
|     4     |    100    | AIN0 | AIN4 |  
|     5     |    101    | AIN1 | AIN4 |  
|     6     |    110    | AIN2 | AIN4 |  
|     7     |    111    | AIN3 | AIN4 |  
+++++++++++++++++++  
++++++TABLE FOR FSR++++++  
+++++++++++++++++++  
| CODE (10) |  CODE (2) |     FSR     |  
|     0     |    000    |   6.144V    |  
|     1     |    001    |   4.096V    |  
|     2     |    010    |   2.048V    |  
|     3     |    011    |   1.024V    |  
|     4     |    100    |   0.512V    |  
|     5     |    101    |   0.256V    |  
+++++++++++++++++++  
++++++TABLE FOR RATE++++++  
+++++++++++++++++++  
| CODE (10) |  CODE (2) |    RATE     |  
|     0     |    000    |    8 SPS    |  
|     1     |    001    |   16 SPS    |  
|     2     |    010    |   32 SPS    |  
|     3     |    011    |   64 SPS    |  
|     4     |    100    |  128 SPS    |  
|     5     |    101    |  250 SPS    |  
|     6     |    110    |  475 SPS    |  
|     7     |    111    |  860 SPS    |  
+++++++++++++++++++  

  These are just a part of them, the whole description is available on the GOOGLE
  

## 1. Measuring
  And then, we'd like to get a lot of data through changing the distance. For this project, we have them stocked in ./src/DATA.py as DATA2. By now, two methodes are provided: interpolation and curve_fit.

## 2. Fitting
  The relation between the distance and the tension should never be linear, while the curve_fit depends a lot on the denseness of x, so we choose to fit the tension with the distance. For the interpolation, there is no difference.

## 3. Prediction
  For curve_fit, as we have already the equation, we can solve this equation and get the distance;while for the interpolation, all we have to do is just calculating the average

