# 2.	Data reading

To be able to treat and analyse the data, we first must read it. This task consisted in the following steps.

1)	Store the CTD files in a particular folder (“data_dirs” variable in the code)
2)	Read the CTD files using the python module “ctd” *
3)	Remove the variables that will not be used in our analysis
4)	Rename the variables to ease the later work
5)	Read the metadata of the CTD files

*Important! The “ctd” python module must be in version 1.1.1. I tried to run the data reading code with the 1.3.0 version, and it did not work. To change its version, introduce the following in the conda console: “conda install -c conda-forge ctd=1.1.1”.
