Folder of the Outliers section 

# 4.	Outliers’ detection and replacement

In statistics, an outlier is a data point that differs significantly from other observations. They may be due to variability in the measurement, or they may indicate experimental error. We should remove them from the dataset as they can cause serious problems in statistical analyses.

Using the functions that we created in the previous section (See section 3), we observed that some vertical profiles contained outliers most likely caused by some instrumental error. Thus, we proceed to find a method to detect and substitute the outlier values. The methodology used to find the appropriate approach was the following. (1) Find a vertical profile that has an evident outlier, (2) apply a determinate approach to detect and substitute the outlier and, if the approach is optimal, (3) repeat the process with all the vertical profiles. Once we detected the outliers, to substitute their values, we used an interpolation between its surrounding points taken from the “scipy” python library (scipy.interpolate.interp1d).

## 4.1 First approach - using 1st derivative
The first approach we tried was based on the characteristic that a single outlier is a value that changes so fast in relation to the two values that surround it. Thus, if we consider the first derivative, an outlier will be surrounded by two “big” derivative values, one positive and the other negative. We established that those “big” derivative values must be bigger than the mean derivative of the profile plus 5 times its standard deviation (we established 5 because if we reduced this number the approach detected too many outliers).

This first approach was appropriate to detect single outliers, however, it had some weak points as it does not correctly detect outliers that are grouped. Thus, we tried to find another approach.

## 4.2	Second approach - using moving mean

This approach detects the outliers using the centered moving mean and moving standard deviation of one vertical profile. It detects as outliers the points that have a value bigger than its moving mean plus 2 times its moving standard deviation. This is a more general approach because it does not detect just single outliers as the previous approach. Nevertheless, we observed that this approach did not work well in the superficial zone. That is because a centered moving mean has not values in the first and last points (contour zones). To solve this, we implemented manually a not centered moving mean for the first values. 

To calculate the moving mean, we used an exponential weight function that “pandas” provides (pandas.DataFrame.ewm) with a window size of 7 values.

Once we detected the outliers, we removed them and replaced them for an interpolated value. This part of the code was a bit complicated because we had to differentiate the single outliers from the group of outliers. For the single outliers, we replaced them for an interpolated value from their surrounding points. For the group of outliers, we calculated an interpolated value from the surrounding points of the whole group and assigned this value to the whole group. In case that the outliers were in the first or last positions, the replaced value was the first or last point that was not an outlier.

This was the approach that prevailed. Thus, we created a function of the whole process and applied it to all the stations and variables.
