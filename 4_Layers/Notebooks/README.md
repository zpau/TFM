Folder to store the notebooks of the Layers' section
Read in the next order: 1-Inflexion_Points 2-MaxMin 3-Classification
The notebooks xxxx_plotting are too make a quick simple analysis of the different approaches

# Layers
The objective of this section is to fins a method to classify the vertical profiles according to their number of water bodies layers. Seawater vertical columns are formed by different water bodies that conform different layers. A water body can be distinguished observing its salinity and temperature values. In this section, we will classify vertical profiles according to their number of layers. In our first two approaches, using the salinity vertical profiles, we will determine the number of layers using the inflexion points and the relative maximums and minimums of the profile, respectively. We use the variable of salinity because the value changes through layers are bigger than using the temperature or density variable.

The steps while doing the approaches where the followings. (1) Find a vertical profile that shows its different layers in a clearly way, (2) smooth the vertical profile to distinguish the big scale features from the small-scale ones, (3) calculate the inflexion points and, finally, (4) obtain the number of layers that form the profile. If the approach worked correctly, we repeated it to the whole set of vertical profiles. It is important to remark that the smoothing exaggeration can affect the result as it can hide smaller layers that we would not underestimate.

## 5.1 1st approach - Inflexion Points
In our first approach, we determine the layers according to the inflexion points of the salinity vertical profiles. Inflexion points are those points where the profile form changes from concave to convex, or vice versa. These points are situated where the second derivative is equal to zero.
The main problem that we observed using this approach was that it detected too many layers in some profiles and if we tried to make the profiles smoother, the approach did not detect adequately the layers in some profiles. Thus, we tried another approach.

## 5.2	2nd approach - Relative maximums and minimums 
This approach uses the relative maximums and minimums to determine the different layers of the vertical profile. The relative maximums and minimums are located where the first derivative is equal to zero.
The file 'maxmin.py' stores a function that resumes this process and returns the number of layers of a particular profile without the plots ('maxmin' function) and with the plots ('maxmin_plot' function).
When we applied this approach to all the profiles, we observed that this approach did not detect as many layers as the first approach and that the results where coherent with what we expected. However, in some profiles it kept detecting too many layers. Thus, we created a variant that grouped the relative maximums or minimums that where closer than 50m (i.e.) and transformed them in just one maximum or minimum centered. This new approach improved made the results more coherent. Anyways, I think that all this new approach could be solved applying more exaggeration into the profile smoothing. We will check it.
We add two functions named "maxmin_2" and "maxmin_2_plot" into the "maxmin.py" file that resumes this 3rd approach without and with plots, respectively.

## 5.3	Layer classification
Once we finished our approaches, we classified all our profiles according to their number of layers.
We created 3 tables, one for each approach. It is important to remark that the results vary significantly in function of how much we smooth the profile. We opted for a significant smooth to observe just the big scale features. To choose how much we smoothed the profile, we used the functions that plot the profiles separated by its layers and decided subjectively which one fit better.
The 3 classifications are similar, especially the second and the third that are almost exact. We could expect it, because when work with very smooth profiles ,the second approach does not detect many layers closer than 50m. Most of the profiles are classified between 3 and 4 layers. Profiles in the first approach range from 2 to 7 layers and in the second and third approaches range from 2 to 6 layers.

In the next section, we will create some maps to observe better those classifications and see if the layer classifications follow any kind of pattern.
