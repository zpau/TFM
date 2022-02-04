def inflexion_points(data, ncast, variable='salinity', lamb=500000):
    """Function that detects the inflexion points
    of a vertical profile and returns the number
    of layers of the profile"""
    #Imports
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    #Smooth the profile with its tendency
    var_cicle, var_tend = sm.tsa.filters.hpfilter(data[ncast][variable],lamb=lamb)
    #Calculate the 2nd derivative
    der2_var_tend = np.diff(var_tend, n=2)
    #Index where are located the inflexion points
    ind_inflexion=[]
    list_ind = []
    for i in range(len(der2_var_tend)):
        if i == (len(der2_var_tend)-1):
            break
        elif (der2_var_tend[i] * der2_var_tend[i+1]) < 0:
            ind_inflexion.append(i)
            ind_inflexion.append(i+1)
            list_ind.append(ind_inflexion)
            ind_inflexion = []
    #Number of layers = the number of inflexion points plus one
    nlayers = len(list_ind)+1
    #Return the numer of layers
    return nlayers




def inflexion_points_plot(data, ncast, variable='salinity', lamb=500000):
    """Function that detects the inflexion points
    of a vertical profile, plots the profile separated
    by its layers and returns the number of layers
    of the profile"""
    #Imports
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    #Smooth the profile with its tendency
    var_cicle, var_tend = sm.tsa.filters.hpfilter(data[ncast][variable],lamb=lamb)
    #Calculate the 2nd derivative
    der2_var_tend = np.diff(var_tend, n=2)
    #Index where are located the inflexion points
    ind_inflexion=[]
    list_ind = []
    for i in range(len(der2_var_tend)):
        if i == (len(der2_var_tend)-1):
            break
        elif (der2_var_tend[i] * der2_var_tend[i+1]) < 0:
            ind_inflexion.append(i)
            ind_inflexion.append(i+1)
            list_ind.append(ind_inflexion)
            ind_inflexion = []
    #Now let's find the depth of these inflexion points
    pres_inflexion = []
    for i in list_ind:
        pres = (data[ncast].index[i[0]] + data[ncast].index[i[1]])/2  
        pres_inflexion.append(pres)
    #Number of layers = the number of inflexion points plus one
    nlayers = len(list_ind)+1
    #Now we plot the result of the profile with its inflexion points
    fig, (ax0, ax1) = plt.subplots(1,2,figsize=(12,7))
    ax0.plot(data[ncast][variable], data[ncast].index)
    ax0.invert_yaxis()
    for i in pres_inflexion:
        ax0.axhline(y=i, c='grey')
    ax0.set_title(ncast+' '+variable)
    ax1.plot(var_tend, data[ncast].index)
    ax1.invert_yaxis()
    for i in pres_inflexion:
        ax1.axhline(y=i, c='grey')
    ax1.set_title(ncast+' Smooth '+variable)
    plt.show()
    #Return the number of layers
    return nlayers