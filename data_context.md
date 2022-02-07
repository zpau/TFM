# Data context

The data used in this TFM was recollected during the TRANSMOW oceanographic cruise where I had the chance to be a part of the scientific crew. 
The TRANSMOW cruise was realized on board of the B.I.O. Hespérides (A-33) research vessel and lasted 21 days from Barcelona to Gijón (from April 28th to May 16th, 2021). 
During the cruise we collected water (from different points of the whole water column) and sediment samples from different points (stations) of the navigation. 
We focus this work on the data collected by the CTD soundings from the 39 stations between the Strait of Gibraltar and Gijón.

The CTD sensor (Conductivity Temperature Depth) samples in continuous the parameters of temperature, salinity (conductivity) and depth, as informs its name, 
but it was also equipped with other sensors to sample others physico-chemical parameters (i.e., dissolved oxygen, pH, turbidity, fluorescence…). 
The CTD sampled the whole water column (from the surface to the seafloor) and stored its data in “.cnv” files (Sea-Bird SBE 9 Data File).

The CTD files contain the register of both sensor descent (downcast) and ascent (upcast). However, we will only read the downcast register. 
The upcast register is commonly discarded because of the potential alteration effects that the CTD mechanism can induce while it is descending. 
The downcast register is considered as a “purer” water sampling.

Now we move on to the python data reading of the CTD files.
