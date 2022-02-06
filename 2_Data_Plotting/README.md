Folder of the Data Plotting section

# 3.	Data plotting
Once we have read the datafiles, we have the dataset ready to be treated and analysed. However, before we get into the data analysis it is important to visualize the data so we can see big scale features or potential outlier values that should be removed. The visualization of the data will help us to do the further analysis and its understanding.

We will learn to plot different graphics of oceanographic interest. The focus will be on plotting vertical profiles (of one or more variables), temperature-salinity diagrams (T-S from now on) and simple vertical sections.

All the plotting functions that have been created have the main function of a quick visualization of the data. They are not designed to create plots ready to be exported and published because they miss some elements (i.e., units in the axis labels). A pending task is to enhance these functions so they can create plots ready to be exported . Nevertheless, we have added an argument in case the plot wants to be exported. 

## 3.1 Vertical profiles
Vertical profiles show how a particular variable is distributed throughout the water column.

To plot vertical profiles, we normally use the built-in function for Data Frames (DF) “DF.plot_cast()” that offers us the python library “pandas”. Nevertheless, to represent vertical profiles of one or more variables, we have created a function based on the “DF.plot_cast()” function and on the “matplotlib.pyplot” python module. The function created can plot a vertical profile of different variables (up to three) in the same graph and with its corresponding axis labels.

We also have created a function to plot the vertical profiles of the whole set of stations, so we can have a quick visualization of the vertical distribution of a particular variable in the whole study zone.

![image](https://user-images.githubusercontent.com/97318159/152702896-b1d11bcd-5b26-49c5-b69f-81fe65fa1a9d.png)
![image](https://user-images.githubusercontent.com/97318159/152702899-931b9e17-e15c-4249-a97c-b8e7e60ba002.png)
![image](https://user-images.githubusercontent.com/97318159/152702904-dce7d3a9-ff86-4f85-a118-e1bdba5db43d.png)

## 3.2	T-S diagrams
T-S diagrams show the relationship between the salinity and the temperature of a water mass body. Temperature and salinity are the main variables that we use to characterize water masses, so these diagrams allow us to see and determine how many water masses are in a particular water body.

We have created a function based on the “matplotlib.pyplot” python module that plots the T-S diagram of one or more stations. It also represents the contours of the anomalies of potential density (sigma density). We have calculated the sigma density using the python library “gsw”.

![image](https://user-images.githubusercontent.com/97318159/152702949-3503d941-7cdd-4384-9bea-fa56792749e5.png)

## 3.3	Vertical sections
Vertical sections show the vertical distribution of a variable along a determined section or transect. Their mechanism is to plot multiple vertical profiles interpolated among them so we could see a 2D slice of a variable vertical distribution.

We have created a function based on a first simple approach that represents vertical sections where the bathymetry is not considered, and the X axis represents the longitudes and not the distance between stations. That makes our vertical sections useful/representative when the sections are well aligned along a same latitude.

The interpolation used is the following from the “scipy” python library: “scipy.interpolate.Rbf()”. This function has different interpolation modes.

![image](https://user-images.githubusercontent.com/97318159/152702956-d7fbc688-1841-4f88-adb7-2aed7737a11e.png)


